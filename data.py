import os
# this script will generate the updated commented, subscribers and posted_id
# lists from their respective .txt files
emptyList = []


def readFile(fileName):
    # check if the file exists(the file wont exist when you use this for the
    # first time) and return and empty list if the file doesn't exist.
    if not os.path.isfile(fileName):
        return emptyList
    # if the file exists, then read the contents of the file and create a list
    # of all the values and return the list.
    with open(fileName, "r") as f:
        someVariable = f.read()
        someVariable = someVariable.split("\n")
        return list(filter(None, someVariable))


def getCommentedList():
    return readFile("commented.txt")


def getSubscribersList():
    return readFile("subscribers.txt")


def getPostedIDsList():
    return readFile("posted_id.txt")
