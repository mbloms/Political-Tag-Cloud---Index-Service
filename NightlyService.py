from twython import TwythonRateLimitError,TwythonError
import time
import ConnectionList as CL
import LoadFollowers as LF
import LoadTweets as LT
import Database
import datetime
import time

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

	def fetchTweets(self):
		self.db.cursor.execute("SELECT userId FROM usr")
		users = self.db.cursor.fetchall()
		counter = 0
		print("Start loading tweets; number of users: " + str(len(users)))
		for user in users:
			counter += 1
			print("#" + str(counter) + " " + str(user[0]))
			start = time.time()
			self.loadTweets.getTweets(user[0])
			end = time.time()
			print("Duration: " + str(end - start))
			print("---")


def main():
	NS = NightlyService()
	NS.fetchTweets()
main()