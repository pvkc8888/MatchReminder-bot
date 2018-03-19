import praw
import re
import time
import os
from reddit_credentials import client_id, client_secret, user_agent, username, password

# Regex compile to extract the twitch links to watch the match.
get = re.compile(r'\[[\w]+\]\(https:\/\/www.twitch.tv\/[\w]+\)')
# make a reddit instance


def reddit_instance():
    reddit = praw.Reddit(client_secret=client_secret,
                         client_id=client_id,
                         password=password,
                         username=username,
                         user_agent=user_agent)
    return reddit


def update_posted(posted_id):
    with open("posts_replied_to.txt", "w") as f:
        f.write(posted_id + "\n")


def look_for_submission(reddit, subreddit, posts_replied_to, users_list):
    # get the latest sumissions from the subreddit
    start_time = 1520658000
    for submission in subreddit.stream.submissions():
        if submission.created > time.time():
            if submission.author == 'MatchReminder-Bot':  # check if the author is the one we want.
                if submission.id not in posted_id:
                    temp = []
                    msg = ''  # if yes, we just print out the title and continue.
                    # print('New submission by D2TournamentThreads: {}', format(submission.title))
                    msg += submission.title
                    msg += '\n'
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
    Now go and enjoy watching some dotes.'''.format(len(users_list)))
                    print('replied to the post : {}'.format(submission.id))
                    posted_id.append(submission.id)
                    print('I replied to {} posts so far.' .format(len(posted_id)))
                    update_posted(submission.id)

                else:
                    pass


def main():
    reddit = reddit_instance()
    print('Reddit instance created with this user: {}'.format(reddit.user.me()))
    # our subreddit is DotA2 pythonforengineers
    subreddit = reddit.subreddit('pythonforengineers')
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
        users_list = []
    look_for_submission(reddit, subreddit, posts_replied_to, users_list)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print('Main not working because of ' + str(e))
