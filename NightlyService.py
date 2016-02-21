from twython import TwythonRateLimitError,TwythonError
import time
import ConnectionList as CL
import LoadFollowers as LF
import LoadTweets as LT
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
		self.conn = CL.ConnectionList(filepath="config/access.conf") 
		self.db = Database.Database()
		self.loadFollowers = LF.LoadFollowers()
		self.loadTweets = LT.LoadTweets()

	def updateFollowers(self):
		self.loadFollowers.getUsersFollowers()
		self.loadFollowers.close()

	def loadTweets(self):
		self.db.cursor.execute("SELECT userId FROM usr")
		users = self.db.cursor.fetchall()
		for user in users:
			print("Fetching tweets for user " + user)
			



def main():
	NS = NightlyService()
	NS.updateFollowers()
main()