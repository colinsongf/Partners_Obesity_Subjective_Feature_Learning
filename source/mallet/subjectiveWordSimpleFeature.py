import mysql.connector

simplePosSubjectivity = """
select 
	hw.ID,
	sl.Word,
	sl.PriorPolarity,
	count(*)
from SubjectiveLexicon sl
join HistoryWordPosNormalized hw
	on sl.Word = hw.Word
group by hw.ID, sl.Word, sl.PriorPolarity
"""

cachedRepoHash = {}

def cacheRepoHash(connection):
	selectCursor = connection.cursor(buffered=True)

	selectCursor.execute(simplePosSubjectivity)

	for row in selectCursor:
		id = int(row[0])
		word = row[1]
		polarity = row[2]
		count = int(row[3])

		wordPolarityKey = "%s~%s" % (word, polarity)

		if cachedRepoHash.has_key(id):
			cachedRepoHash[id][wordPolarityKey] = count
		else:
			cachedRepoHash[id] = { wordPolarityKey: count }


def get(data):
	id = data[0]
	returnVector = []
	if cachedRepoHash.has_key(id):
		for key in cachedRepoHash[id]:
			returnVector.append("%s %s" % (key, cachedRepoHash[id][key]))

	return " ".join(returnVector)






