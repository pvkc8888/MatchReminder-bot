from data import *
import time

addEntryInSubscribersList("hey")
for item in getSubscribersList():
	print item

time.sleep(100)