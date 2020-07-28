# Product name class used in receipt table
PRODUCT_NAME_TAG = 'product-name'

# Product total cost class used in receipt table
PRODUCT_TOTAL_TAG = 'col-total price'

# Opens the receipt and virtualises file
receipt = open('resources/sample_004.txt')

# Closest start and end line for shopping receipt data
startLine = 0
endLine = 0

# Fields for items in shopping receipt
names = []
costs = []

# Used to track current line number in loop
lineIndex = 0

# Tell line reading loop to add name/cost/etc to lists
nameDetected = False
costDetected = False

# Line number to capture for name/cost/count lists
lineToCapture = 0

# Gets line numbers for closest identifiable tags that surround the shopping list elements in receipt code #
for line in receipt:

    # If the lien number is right and a name was detected, clean the line up and add it to the names list
    if nameDetected and lineIndex == lineToCapture:
        names.append(line.strip().replace('&amp;', '&').replace('  ', ' ').replace('&#39;', "'"))
        nameDetected = False
        lineToCapture = 0

    # If the lien number is right and a cost was detected, clean the line up and add it to the costs list
    if costDetected and lineIndex == lineToCapture:
        costs.append(float(line.strip().strip('$')))
        costDetected = False
        lineToCapture = 0

    # If the tag denoting a product name was detected, set line to capture for the names list
    if PRODUCT_NAME_TAG in line:
        nameDetected = True
        lineToCapture = (lineIndex + 1)

    # If the tag denoting a product cost was detected, set line to capture for the costs list
    if PRODUCT_TOTAL_TAG in line:
        costDetected = True
        lineToCapture = (lineIndex + 2)

    # Increment line number index
    lineIndex += 1

    # Debug messages
print(names)

print('')

print(costs)
