commentedList = []
subscribersList = []
postedIDsList = []	


def readFile(fileName):
    with open(fileName, "r") as f:
        someVariable = f.read()
        someVariable = someVariable.split("\n")
        return list(filter(None, someVariable))


commentedList = readFile("commented.txt")
subscribersList = readFile("subscribers.txt")
postedIDsList = readFile("posted_id.txt")


def getCommentedList():
    return commentedList;

def getSubscribersList():
    return subscribersList;

def getPostedIDsList():
    return postedIDsList;


def addEntryInCommentedList(value):
    commentedList.append(value)

def addEntryInSubscribersList(value):
    subscribersList.append(value)

def addEntryInPostedIDsList(value):
    postedIDsList.append(value)

