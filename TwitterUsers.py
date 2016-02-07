import json
class TwitterUsers:
	"List of TwitterUsers"
	def __init__(self):
		self.configPath = "config/accounts.config.json"
		self.dict = self.prepareData()
		
	def prepareData(self):
		"Load config file and store as JSON object"
		with open(self.configPath, 'r', encoding='utf8') as data_file:
			data = json.load(data_file)
			data_file.close()
		return data

	def getGroups(self):
		"Return the items in JSON file"
		return self.dict.items()

	def getGroup(self, groupName):
		"Return list of user IDs of specific group"
		try :
			group = self.dict[groupName]
		except KeyError:
			print("Group " + groupName + " not found")
			return 0
		return group

	def addGroup(self, groupName): 
		"Add group with name groupName"
		self.dict[groupName] = {'users': []}
		self.save()

	def deleteGroup(self, groupName):
		"Delete group with name groupName"
		try:
			self.dict.pop(groupName)
			self.save()
			return 1
		except KeyError:
			print("Group " + groupName + " not found")
			return 0


	def addUserToGroup(self, groupName, userID):
		"Add user to group with name groupName and ID userID"
		try:
			self.dict[groupName]['users'].append(userID)
			self.save()
		except KeyError:
			print("Group " + groupName + " not found")
			return 0
		return 1

	def deleteUserFromGroup(self, groupName, userID):
		"Delete user from group with name groupName and ID userID"
		for i in range(len(self.dict[groupName]['users'])):
			if self.dict[groupName]['users'][i] == userID:
				self.dict[groupName]['users'].pop(i)
				self.save()
				break

	def save(self):
		with open(self.configPath, 'w', encoding='utf8') as outfile:
			json.dump(self.dict, outfile)