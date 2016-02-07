# Using Twithon, install with sudo pip3 install twython
from twython import Twython
import twythonHelper

class ConnectionList:
	"List of (Twython) objects that rotates every time a 'connection' is extracted."
	def __init__(self,arr = [], filepath = ""):
		if filepath != "" or arr == []:
			arr = readFile(filepath)
		#The array with all objects
		self.arr = arr
		#Start index
		self.index = 0

	def connection(self):
		"Rotates the index value and returns the object at that index"
		self.__rotate()
		return self.arr[self.index]
	def __rotate(self):
		self.index = (self.index + 1) % len(self.arr)

def readFile(filepath):
	lst = []
	txt = open(filepath, 'r')
	#Read first line
	line = txt.readline()
	#While there is more
	while line != "":
		#Make Twython objects of two lines, ignoring the first of three. If the lines in the file is not devisable by 3, something will go bad.
		lst.append(twythonHelper.newTwython(txt.readline, txt.readline))
		line = txt.readline()
	txt.close()
	return lst