import os

emptyList = []

def readFile(fileName):
	if not os.path.isfile(fileName):
		return emptyList
	with open(fileName, "r") as f:
		someVariable = f.read()
		someVariable = someVariable.split("\n")
		return list(filter(None, someVariable))

def getCommentedList():
	return readFile("commented.txt")

def getSubscribersList():
	return readFile("subscribers.txt");	

def getPostedIDsList():
	return readFile("posted_id.txt")
