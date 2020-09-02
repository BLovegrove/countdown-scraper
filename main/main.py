from tabulate import tabulate
import os
import sys

from testing import receiptTest
from receipt import Receipt
from userlist import UserList

os.system('cls' if os.name == 'nt' else 'clear')

print("Please enter the location of the receipt: ")
receiptLocation = input(">>>")

receipt = Receipt(receiptLocation, 'data/config.json')
users = UserList("data/users.json")

# Learn any new items
for item in receipt.productNames:
	for user in users.names:
		if item not in users.data[user][0].keys():
			print("")
			print(user + ": " + item + " not recognised. Enter contribution as a fraction:")

			# Fetch item data and display it
			itemDetails = receipt.getItemDetails(item)
			if itemDetails != False:
				print("Item details:")
				print(itemDetails)
			else:
				print("Error: Item details not found")

			while True:
				try:
					contribution = eval(input(">>>"))
					break
				except SyntaxError:
					print("Error: Not a valid fraction. Try again.")
			users.data[user][0][item] = contribution

# Save learned data
users.dumpJson()

# Compare and compute shopping [item name, total cost, {user costs}]
breakdownData = []
breakdownDataHeader = ["Item name", "Total cost"]

# Add user's contributions to header
for user in users.names:
	breakdownDataHeader.append(user + "'s contribution")

# Add product total costs to data
for item in receipt.productNames:
	breakdownRow = []
	breakdownRow.append(item)

	itemData = receipt.getItem(item)
	if itemData != 404:
		breakdownRow.append(itemData[3])
	else:
		print("Error: Item doesn't exist")
		print(itemData)
		break

	# Add user contributions to data
	for user in users.names:

		contribution = users.getItemContribution(user, item)
		if contribution != 404:
			breakdownRow.append(contribution * itemData[3])
		else:
			print("Error: " + user + "'s contribution for this item doesn't exist")
			print(contribution)
			break

	# Add row set to main data set
	breakdownData.append(breakdownRow)

# Cost breakdown totals
breakdownTotals = [round(receipt.shopCost, 2)]
breakdownTotalsHeader = ["Total cost"]

# Add user's contributions to headers
for user in users.names:
	breakdownTotalsHeader.append(user + "'s Total")

# Calculate totals for individual users against total for the whole shop
for i in range((len(breakdownDataHeader) - len(users.names)), len(breakdownDataHeader)):

	cost = 0

	for item in breakdownData:
		cost += item[i]

	breakdownTotals.append(round(cost, 2))

# Add unaccounted money to the header
breakdownTotalsHeader.append("Unaccounted")

unaccountedTotal = breakdownTotals[0]

# Calculate money unaccounted for by any user
for i in range((len(breakdownTotals) - len(users.names)), len(breakdownTotals)):
	unaccountedTotal -= breakdownTotals[i]

breakdownTotals.append(round(unaccountedTotal, 2))

# Add dollar ($) signs to the data set
itemIndex = 0
for item in breakdownData:
	valueIndex = 0
	for value in item:
		if type(value) is int or type(value) is float:
			breakdownData[itemIndex][valueIndex] = "$" + str(breakdownData[itemIndex][valueIndex])
		valueIndex += 1
	itemIndex += 1

itemIndex = 0
for item in breakdownTotals:
	breakdownTotals[itemIndex] = "$" + str(breakdownTotals[itemIndex])
	itemIndex += 1

# Print data sets in pretty tables
print("")
print(tabulate(breakdownData, headers=breakdownDataHeader, tablefmt="fancy_grid", numalign="left"))
print("")

print("")
print(tabulate([breakdownTotals], headers=breakdownTotalsHeader, tablefmt="fancy_grid", numalign="left"))
print("")
