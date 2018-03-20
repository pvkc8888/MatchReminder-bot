import praw
import re
import time
import os.path
from reddit_credentials import client_id, client_secret, user_agent, username, password


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

# make a reddit instance


def reddit_instance():
    reddit = praw.Reddit(client_secret=client_secret,
                         client_id=client_id,
                         password=password,
                         username=username,
                         user_agent=user_agent)
    return reddit

# update the posted text file with the lastest submission id


def update_comments(comment_id):
    with open("commented.txt", "a") as f:
        f.write(str(comment_id) + "\n")
        print('New comment_id {} has been added to the list' .format(str(comment_id)))


def update_subs(comment_author):
    with open("subscribers.txt", "a") as f:
        f.write(str(comment_author) + "\n")
        print('New redditor {} has been added to the list' .format(str(comment_author)))


def look_for_subscribers(reddit, subreddit, posted_id):
    for post in posted_id:
        print('looking for this post')
        parent = None
        submission = reddit.submission(post)
        for comment in submission.comments.list():
            print(str(comment.parent()), parent)
            if comment.author == 'MatchReminder-bot' and str(comment.parent()) == post:
                print('parent before me')
                parent = str(comment.id)
                print('Im the original parent', parent)
                # print(commented)
            # if comment.parent == parent:
            #     print('parent is working')
            if comment.body.lower() == '!addme' and str(comment.parent()) == parent and comment.id not in commented:
                print('stage3')
                if comment.author not in subscribers:
                    print('stage4')
                    update_subs(comment.author)
                    comment.reply('Added!')
                    print('stage5')
                    update_comments(comment.id)
                    print('New user {} added to the subscribers list'.format(comment.author))
                else:
                    comment.reply('You are already in the Subscribers list!')
                    print('user {} already in the subscribers list'.format(comment.author))
    time.sleep(10)


def main():
    reddit = reddit_instance()
    print('Reddit instance created with this user: {}'.format(reddit.user.me()))

    # our subreddit is DotA2 pythonforengineers
    subreddit = reddit.subreddit('pythonforengineers')
    look_for_subscribers(reddit, subreddit, posted_id)
    time.sleep(30)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print('Main not working because of ' + str(e))
