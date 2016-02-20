from twython import TwythonRateLimitError,TwythonError
import time
import ConnectionList as CL
import LoadFollowers as LF
import Database
import datetime

class NightlyService:
	""" 
		The frame for our Nightly service with these main functions:
		• Update list of followers to our groups
		• Fetch tweets for new users
		• Update tweets for already existing users
	"""
	def __init__(self):
		pass

	def updateFollowers(self):
		loadFollowers = LF.LoadFollowers()
		loadFollowers.getUsersFollowers()
		loadFollowers.close()

def main():
	NS = NightlyService()
	NS.updateFollowers()
main()