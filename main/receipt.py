import json

class Receipt:

	def __init__(self, file, config):

		self.data = open(file)
		self.settings = json.load(open(config))

		self.productNames = []
		self.unitCosts = []
		self.quantities = []
		self.totalCosts = []

		self.shopCost = 0

		self.processData()
		self.calculateShopCost()

	def processData(self):

		# Used to track current line number in loop
		lineIndex = 0

		# Tell line reading loop to add name/cost/etc to lists
		nameDetected = False
		unitDetected = False
		quantityDetected = False
		costDetected = False

		# Line number to capture for name/cost/count lists
		lineToCapture = 0

		# Gets line numbers for closest identifiable tags that surround the shopping list elements in receipt code #
		for line in self.data:

				# If the line number is right and a name was detected, clean the line up and add it to the names list
				if nameDetected and lineIndex == lineToCapture:
					self.productNames.append(line.strip().replace(
							'&amp;', '&').replace('  ', ' ').replace('&#39;', "'"))
					nameDetected = False
					lineToCapture = 0

				# If the line number is right and a unit cost was detected, clean the line up and add it to the unit costs list
				if unitDetected and lineIndex == lineToCapture:
					self.unitCosts.append(line.strip().strip('$').replace(' ea', '').replace(' kg', ''))
					unitDetected = False
					lineToCapture = 0

				# If the line number is right and a quantity was detected, clean the line up and add it to the unit costs list
				if quantityDetected and lineIndex == lineToCapture:
					if line.strip() != 'Qty':
						self.quantities.append(float(line.strip().replace(' kg', '')))
					quantityDetected = False
					lineToCapture = 0

				# If the line number is right and a cost was detected, clean the line up and add it to the costs list
				if costDetected and lineIndex == lineToCapture:
					self.totalCosts.append(float(line.strip().strip('$')))
					costDetected = False
					lineToCapture = 0

				# If the tag denoting a product name was detected, set line to capture for the names list
				if self.settings["tags"][0]["product name"] in line:
					nameDetected = True
					lineToCapture = (lineIndex + 1)

				# If the tag denoting a product unit cost was detected, set line to capture for the costs list
				if self.settings["tags"][0]["unit cost"] in line:
					unitDetected = True
					lineToCapture = (lineIndex + 2)

				# If the tag denoting a product quantity was detected, set line to capture for the costs list
				if self.settings["tags"][0]["quantity"] in line:
					quantityDetected = True
					lineToCapture = (lineIndex + 1)

				# If the tag denoting a product cost was detected, set line to capture for the costs list
				if self.settings["tags"][0]["total cost"] in line:
					costDetected = True
					lineToCapture = (lineIndex + 2)

				# Increment line number index
				lineIndex += 1

		# Clean quantity duplicates
		self.quantities = self.quantities[::2]

	def calculateShopCost(self):

		for cost in self.totalCosts:
			self.shopCost += cost

	def getItem(self, itemName):

		index = 0
		for item in self.productNames:
			if item == itemName:
				break

			index += 1

		if index == len(self.productNames):
			return 404
		else:
			return [self.productNames[index], self.unitCosts[index], self.quantities[index], self.totalCosts[index]]

	def getItemDetails(self, itemName):

		index = 0
		for item in self.productNames:
			if item == itemName:
				break
			
			index += 1

		if (index) == len(self.productNames):
			return False
		else:
			return "[Unit price: " + str(self.unitCosts[index]) + ", Qauntity: " + str(self.quantities[index]) + ", Total cost: " + str(self.totalCosts[index]) + "]"
	
