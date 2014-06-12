import re

whiteSpace = "\\s+"

limitCount = 70

uniqueWordsSql = """
select 
	word
from patientdischarge.diseaseuniquewords
"""

wordFeatures = []

def cacheRepoHash(connection):
	selectCursor = connection.cursor(buffered=True)

	selectCursor.execute(uniqueWordsSql)

	for row in selectCursor:
		wordFeatures.append(row[0])

def get(data):
	featureWordDict = {}

	for wordFeature in wordFeatures:
		featureWordDict[wordFeature] = 0

	for word in re.split(whiteSpace, data[1]):
		if featureWordDict.has_key(word):
			featureWordDict[word] = featureWordDict[word] + 1

	returnArray = []
	for wordKey in featureWordDict:
		if featureWordDict[wordKey] > limitCount:
			returnArray.append("%s %s" % (wordKey, 1))
		else:
			returnArray.append("%s %s" % (wordKey, 0))

	return " ".join(returnArray)