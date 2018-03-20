import praw
import re
import time
import os.path
from reddit_credentials import client_id, client_secret, user_agent, username, password
from data import *

##TODOs
#1.  Change print to a function where it would write to a file
#2.  


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


def look_for_subscribers(reddit):
    posted_id = list(getPostedIDsList())
    subscribers = getSubscribersList()[:]
    commented = getCommentedList()[:]
    for post in posted_id:
        print('looking for this post' + post)
        parent = None
        submission = reddit.submission(post)
        for comment in submission.comments.list():
            print(str(comment.parent()), parent)
            if comment.author == 'MatchReminder-bot' and str(comment.parent()) == post:
                print('parent before me')
                parent = str(comment.id)
                print('Im the original parent', parent)
            if comment.body.lower() == '!addme' and str(comment.parent()) == parent and comment.id not in commented:
                print('stage3')
                if comment.author not in subscribers:
                    print('stage4')
                    update_subs(comment.author)
                    subscribers.append(comment.author)
                    comment.reply('Added!')
                    print('stage5')
                    update_comments(comment.id)
                    commented.append(comment.id)
                    print('New user {} added to the subscribers list'.format(comment.author))
                else:
                    comment.reply('You are already in the Subscribers list!')
                    print('user {} already in the subscribers list'.format(comment.author))
                    commented.append(comment.id)
                    update_comments(comment.id)
    time.sleep(10)


def main():
    reddit = reddit_instance()
    print('Reddit instance created with this user: {}'.format(reddit.user.me()))
    look_for_subscribers(reddit)
    time.sleep(30)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print('Main not working because of ' + str(e))
