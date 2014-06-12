import mysql.connector

complexPosSubjectivity = """
select 
	hw.ID,
	sl.Word,
	sl.Type,
	sl.PriorPolarity,
	count(*)
from SubjectiveLexicon sl
join HistoryWordPosNormalized hw
	on sl.Word = hw.Word
group by hw.ID, sl.Type, sl.Word, sl.PriorPolarity
"""

cachedRepoHash = {}

def cacheRepoHash(connection):
	selectCursor = connection.cursor(buffered=True)

	selectCursor.execute(complexPosSubjectivity)

	for row in selectCursor:
		id = int(row[0])
		word = row[1]
		pType = row[2]
		polarity = row[3]
		count = int(row[4])

		wordPolarityTypeKey = "%s~%s~%s" % (word, polarity, pType)

		if cachedRepoHash.has_key(id):
			cachedRepoHash[id][wordPolarityTypeKey] = count
		else:
			cachedRepoHash[id] = { wordPolarityTypeKey: count }


def get(data):
	id = data[0]
	returnVector = []
	if cachedRepoHash.has_key(id):
		for key in cachedRepoHash[id]:
			returnVector.append("%s %s" % (key, cachedRepoHash[id][key]))

	return " ".join(returnVector)






