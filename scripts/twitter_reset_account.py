#!/usr/bin/python
# (C) 2013 Julian Metzler

"""
This script resets a Twitter account to zero
"""

import base64
import tweetpony

from StringIO import StringIO

BLACK = """iVBORw0KGgoAAAANSUhEUgAAAJYAAACWCAIAAACzY+a1AAAACXBIWXMAAAsTAAALEwEAmpwYAAAA
B3RJTUUH3QUfFBUHEBAV8wAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAABY
SURBVHja7cExAQAAAMKg9U9tB2+gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgMQhRAAGQ5RxKAAAAAElFTkSuQmCC"""

def main():
	api = tweetpony.API(tweetpony.CONSUMER_KEY, tweetpony.CONSUMER_SECRET)
	url = api.get_auth_url()
	print "Visit this URL to login: %s" % url
	verifier = raw_input("PIN: ")
	api.authenticate(verifier)
	if not raw_input("This will UNFOLLOW all people, temporarily BLOCK and UNBLOCK your followers so you lose them, DELETE all your tweets and direct messages and RESET your profile information.\nContinue? [y/N] ").lower() == "y":
		return
	
	print "Unfollowing..."
	try:
		following_ids = api.friends_ids()
	except:
		print "Error\n"
	else:
		for id in following_ids:
			api.unfollow(user_id = id)
			print id
		print "Done\n"
	
	print "Losing followers..."
	try:
		follower_ids = api.followers_ids()
	except:
		print "Error\n"
	else:
		for id in follower_ids:
			api.block(user_id = id)
			api.unblock(user_id = id)
			print id
		print "Done\n"
	
	print "Deleting tweets..."
	tweets = [None]
	while len(tweets) > 0:
		try:
			tweets = api.user_timeline(user_id = api.user.id, count = 1000)
		except:
			print "Error\n"
		else:
			for tweet in tweets:
				tweet.delete()
				print tweet.text.encode('utf-8').replace("\n", " ")
			print "Done\n"
	
	print "Deleting sent direct messages..."
	messages = [None]
	while len(messages) > 0:
		try:
			messages = api.sent_messages(count = 1000)
		except:
			print "Error\n"
		else:
			for message in messages:
				message.delete()
				print "@%s %s" % (message.receiver.screen_name, message.text.encode('utf-8').replace("\n", " "))
			print "Done\n"
	
	print "Deleting received direct messages..."
	messages = [None]
	while len(messages) > 0:
		try:
			messages = api.received_messages(count = 1000)
		except:
			print "Error\n"
		else:
			for message in messages:
				message.delete()
				print "[%s] %s" % (message.receiver.screen_name, message.text.encode('utf-8').replace("\n", " "))
			print "Done\n"
	
	print "Resetting profile information..."
	try:
		api.update_profile(name = "Name", description = "Bio", url = "http://www.example.com/", location = "Location")
		api.update_profile_image(image = StringIO(base64.b64decode(BLACK)))
		api.update_background(use = False)
		api.remove_profile_banner()
	except:
		print "Error\n"
	else:
		print "Done\n"

if __name__ == "__main__":
	main()