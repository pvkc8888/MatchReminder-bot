import praw
import re
import time
import os.path
from reddit_credentials import client_id, client_secret, user_agent, username, password
from data import *


# Regex compile to extract the twitch links of the stream to watch the match.
get = re.compile(r'\[[\w]+\]\(https:\/\/www.twitch.tv\/[\w]+\)')

# this function will send private message to the users who are already in the
# subscribers list


def send_message(reddit, message_subject, message_body, subscribers):
    for user in subscribers:
        try:
            final_body = 'Hey, u/{}. The wait is over. '.format(user) + message_body
            reddit.redditor(user).message(message_subject, final_body)
        except Exception as e:
            print('System warning - ' + str(e))
            pass


# make a reddit instance
def reddit_instance():
    reddit = praw.Reddit(client_secret=client_secret,
                         client_id=client_id,
                         password=password,
                         username=username,
                         user_agent=user_agent)
    return reddit

# update the posted text file with the lastest submission id so that we know
# that we have already commented on that post


def update_posted(post_id):
    with open("posted_id.txt", "a") as f:
        f.write(post_id + "\n")
        print('New submission with id {} has been added' .format(post_id))

# This function will stream through all the submissions in r/DotA2 and call
# subsequent functions if necessary.


def look_for_submission(reddit, subreddit):
    for submission in subreddit.stream.submissions():
        posted_id = getPostedIDsList()[:]
        subscribers = getSubscribersList()[:]
        commented = getCommentedList()[:]
        if submission.created_utc > startTime:
            # check if the author is the one we want.
            if submission.author == 'D2TournamentThreads':
                # check if we have already commented on that post to make sure
                # we dont spam reddit!
                if submission.id not in posted_id:
                    # yes, so its a new thread, so we continue with making a new
                    # message that we send to the subsribers
                    temp = []
                    msg = ''
                    msg += submission.title
                    msg += ' matches have begun, \n'
                    # check the submission.selftext to extract the stream links.
                    found = get.findall(submission.selftext)
                    # if there are stream links, go inside the if loop and add
                    # them to the message
                    if found:
                        msg += 'You can watch the stream in any of the following links: \n'
                        for item in found:
                            if item not in temp:
                                msg += item
                                msg += '\n'
                                temp.append(item)
                    else:
                        # if no stream links, just add no stream links found
                        msg += 'No twitch links found \n'
                    msg += 'For more info on the matches, visit this reddit thread [here]({}) \n'.format(submission.url)
                    # debug check to make sure its working
                    print(msg)
                    # we reply to the new submission asking for new users to
                    # subscribe
                    submission.reply('''I am a MatchReminder-Bot that reminds users when a DotA match is about to start. To get subscribed to the list of {} users, reply with "!addme" to this comment and you will be added to the list and reminded from the next post.
    For feedback, please PM me [here](https://www.reddit.com/message/compose/?to=matchreminder-bot).
    Now go and enjoy watching some dotes.'''.format(len(subscribers)))
                    print('replied to the post : {}'.format(submission.id))
                    # call posted_if function and append this submission.id so
                    # that we know we have already commented on this.
                    posted_id.append(submission.id)
                    update_posted(submission.id)
                    print('I replied to {} posts so far.' .format(len(posted_id)))
                    # Now send message to the subscribers that matches are
                    # about to start
                    send_message(reddit, submission.title, msg, subscribers)
                    print("I'm done posting and asking for new users to subscribe, time to sleep!!!!!")
                    time.sleep(60)
            else:
                time.sleep(30)
                pass


startTime = time.time()


def main():
    reddit = reddit_instance()
    # Log check
    print('Reddit instance created with this user: {}'.format(reddit.user.me()))
    # our subreddit is DotA2
    subreddit = reddit.subreddit('DotA2')
    look_for_submission(reddit, subreddit)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print('Main not working because of ' + str(e))
        time.sleep(30)
