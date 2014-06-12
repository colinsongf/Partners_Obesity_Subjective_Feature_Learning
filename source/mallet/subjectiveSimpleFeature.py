import mysql.connector

simpleSubjectivity = """
select 
	hw.ID,
	case 
		when sl.PriorPolarity is null then 'none'
		else sl.PriorPolarity
	end as Polarity,
	count(*)
from SubjectiveLexicon sl
right outer join geniatuple hw
	on sl.Word = hw.base
group by hw.ID, sl.PriorPolarity
"""

cachedRepoHash = {}

def cacheRepoHash(connection):
	selectCursor = connection.cursor(buffered=True)

	selectCursor.execute(simpleSubjectivity)

	for row in selectCursor:
		id = int(row[0])
		polarity = row[1]
		count = int(row[2])

		if cachedRepoHash.has_key(row[0]):
			cachedRepoHash[id][polarity] = count
		else:
			cachedRepoHash[id] = { polarity: count }


def get(data):
	id = data[0]
	returnVector = []
	if cachedRepoHash.has_key(id):
		for key in cachedRepoHash[id]:
			returnVector.append("%s %s" % (key, cachedRepoHash[id][key]))

	return " ".join(returnVector)






