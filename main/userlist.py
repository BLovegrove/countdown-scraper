import json

class UserList:

	def __init__(self, dataFile):

		self.dataFile = dataFile
		self.data = json.load(open(dataFile))

		self.names = []

		self.populateNames()

	def populateNames(self):

		for key in self.data.keys():
			self.names.append(key)

	def getItemContribution(self, userName, itemName):

		for name in self.names:
			if name == userName:
				for key, value in self.data[userName][0].items():
					if key == itemName:
						return value
		
		return 404

	def dumpJson(self):

		with open(self.dataFile, 'w', encoding='utf-8') as f:
			json.dump(self.data, f, ensure_ascii=False, indent=2)
