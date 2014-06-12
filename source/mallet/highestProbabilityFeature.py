import re

whiteSpace = "\\s+"

uniqueWordsSql = """
select 
	Word,
	Disease,
	AvgProb
from diseasehighestprobwords
"""

cachedRepoHash = {}

def cacheRepoHash(connection):
	selectCursor = connection.cursor(buffered=True)

	selectCursor.execute(uniqueWordsSql)

	for row in selectCursor:
		word = row[0]
		prob = float(row[2])
		cachedRepoHash[word] = prob

def get(data):
	featureWordDict = {}

	for word in cachedRepoHash:
		featureWordDict[word] = 0

	count = 0
	for word in re.split(whiteSpace, data[1]):
		count = count + 1
		if featureWordDict.has_key(word):
			featureWordDict[word] = featureWordDict[word] + 1

	count = float(count)
	returnArray = []
	for wordKey in featureWordDict:
		if (featureWordDict[wordKey] / count) >= cachedRepoHash[wordKey]:
			returnArray.append("PROB%s %s" % (wordKey, 1))
		# else:
			# returnArray.append("%s %s" % (wordKey, 0))

	return " ".join(returnArray)