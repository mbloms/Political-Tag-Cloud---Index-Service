class ConnectionList:
	"List of (Twython) objects that rotates every time a 'connection' is extracted."
	def __init__(self,arr):
		#The array with all objects
		self.arr = arr
		#Start index
		self.index = 0
		#Size of the array
		self.size = len(arr)

	def connection(self):
		"Rotates the index value and returns the object at that index"
		self.__rotate()
		return self.arr[self.index]
	def __rotate(self):
		self.index = (self.index + 1) % self.size