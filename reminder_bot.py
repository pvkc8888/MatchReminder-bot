import praw
import re
import time
import os.path
from reddit_credentials import client_id, client_secret, user_agent, username, password
from data import *

if not os.path.isfile("subscribers.txt"):
    subscribers = []
else:
    # Read the file into a list and remove any empty values
    with open("subscribers.txt", "r") as f:
        subscribers = f.read()
        subscribers = subscribers.split("\n")
        subscribers = list(filter(None, subscribers))

if not os.path.isfile("posted_id.txt"):
    posted_id = []
else:
    # Read the file into a list and remove any empty values
    with open("posted_id.txt", "r") as f:
        posted_id = f.read()
        posted_id = posted_id.split("\n")
        posted_id = list(filter(None, posted_id))

if not os.path.isfile("commented.txt"):
    commented = []
else:
    # Read the file into a list and remove any empty values
    with open("commented.txt", "r") as f:
        commented = f.read()
        commented = commented.split("\n")
        commented = list(filter(None, commented))

# Regex compile to extract the twitch links to watch the match.
get = re.compile(r'\[[\w]+\]\(https:\/\/www.twitch.tv\/[\w]+\)')


def send_message(reddit, message_subject, message_body):
    # Sends the messages to the subscribed users
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

# update the posted text file with the lastest submission id


def update_posted(post_id):
    with open("posted_id.txt", "a") as f:
        f.write(post_id + "\n")
        print('New submission with id {} has been added' .format(post_id))


def look_for_submission(reddit, subreddit, posted_id):
    # get the latest sumissions from the subreddit
    for submission in subreddit.stream.submissions():
        if submission.created > time.time():
            if submission.author == 'MatchReminder-Bot':  # check if the author is the one we want.
                if submission.id not in posted_id:
                    temp = []
                    msg = ''  # if yes, we just print out the title and continue.
                    # print('New submission by D2TournamentThreads: {}', format(submission.title))
                    msg += submission.title
                    msg += ' matches have begun, \n'
                    # check the submissions selftext to extract the stream links.
                    found = get.findall(submission.selftext)
                    # if there are stream links, continue
                    if found:
                        msg += 'You can watch the stream in any of the following links: \n'
                        for item in found:
                            if item not in temp:
                                msg += item
                                msg += '\n'
                                temp.append(item)
                    else:
                        msg += 'No twitch links found \n'
                    msg += 'For more info on the matches, visit this reddit thread [here]({}) \n'.format(submission.url)
                    print(msg)
                    submission.reply('''I am a MatchReminder-Bot that reminds users when a DotA match is about to start. To get subscribed to the list of {} users, reply with "!addme" to this comment and you will be added to the list and reminded from the next post.
    For feedback, please PM me [here](https://www.reddit.com/message/compose/?to=matchreminder-bot).
    Now go and enjoy watching some dotes.'''.format(len(posted_id)))  # change this back to users list
                    print('replied to the post : {}'.format(submission.id))
                    posted_id.append(submission.id)
                    print('I replied to {} posts so far.' .format(len(posted_id)))
                    update_posted(submission.id)
                    send_message(reddit, submission.title, msg)
                    print("I'm done posting and asking for new users to subscribe, time to sleep!!!!!")
                    time.sleep(60)
            else:
                time.sleep(30)
                pass


def main():
    reddit = reddit_instance()
    print('Reddit instance created with this user: {}'.format(reddit.user.me()))
    # our subreddit is DotA2 pythonforengineers
    subreddit = reddit.subreddit('pythonforengineers')
    look_for_submission(reddit, subreddit, posted_id)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print('Main not working because of ' + str(e))
        time.sleep(30)
