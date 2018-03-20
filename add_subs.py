import praw
import re
import time
import os.path
from reddit_credentials import client_id, client_secret, user_agent, username, password
from data import *

# creating a reddit instance


def reddit_instance():
    reddit = praw.Reddit(client_secret=client_secret,
                         client_id=client_id,
                         password=password,
                         username=username,
                         user_agent=user_agent)
    return reddit

# update the commented text file with the lastest comment id


def update_comments(comment_id):
    with open("commented.txt", "a") as f:
        f.write(str(comment_id) + "\n")
        print('New comment_id {} has been added to the list' .format(str(comment_id)))

# update the subscribers text file with new subs.


def update_subs(comment_author):
    with open("subscribers.txt", "a") as f:
        f.write(str(comment_author) + "\n")
        print('New redditor {} has been added to the list' .format(str(comment_author)))

# go through all the posts that I made and find any new subscribers.


def look_for_subscribers(reddit):
    # get the lastes lists from the data.py file

    posted_id = list(getPostedIDsList())
    subscribers = getSubscribersList()[:]
    commented = getCommentedList()[:]
    # get each submission from the posted_id list
    for post in posted_id:
        print('looking for this post' + post)
        parent = None
        submission = reddit.submission(post)
        # go through each comment in that submission
        for comment in submission.comments.list():
            # check if its our parent post
            if comment.author == 'MatchReminder-bot' and str(comment.parent()) == post:
                parent = str(comment.id)
                print('Im the original parent: ', parent)
            # check for all comments that are children to our comment and have !addme
            # in their body and are not already in the commented list
            if comment.body.lower() == '!addme' and str(comment.parent()) == parent and comment.id not in commented:
                # if the author is not in subs list, we have to add him
                if comment.author not in subscribers:
                    update_subs(comment.author)
                    subscribers.append(comment.author)
                    # tell him that he's added
                    comment.reply('Added!')
                    update_comments(comment.id)
                    commented.append(comment.id)
                    print('New user {} added to the subscribers list'.format(comment.author))
                else:
                    # if the user is already in the list, tell him that!
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
