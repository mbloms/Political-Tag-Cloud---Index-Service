import json
class DatabaseConfig:
	def __init__(self,path,name):
		db = self.readConf(path,name)
		self.database = db["database"]
		self.user = db["user"]
		self.password = db["password"]
		self.host = db["host"]
		self.port = db["port"]
	def readConf(self,path,name):
		f = open(path,"r") 
		databases = json.load(f)
		database = databases[name]
		return database
