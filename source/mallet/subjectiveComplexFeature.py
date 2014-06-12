import mysql.connector

complexSubjectivity = """
select 
	hw.ID,
	case 
		when sl.Type is null then 'none'
		else sl.Type
	end Type,
	case 
		when sl.PriorPolarity is null then 'none'
		else sl.PriorPolarity
	end Polarity,
	count(*)
from SubjectiveLexicon sl
right outer join geniatuple hw
	on sl.Word = hw.base
group by hw.ID, sl.Type, sl.PriorPolarity
"""

cachedRepoHash = {}

def cacheRepoHash(connection):
	selectCursor = connection.cursor(buffered=True)

	selectCursor.execute(complexSubjectivity)

	for row in selectCursor:
		id = int(row[0])
		pType = row[1]
		polarity = row[2]
		count = int(row[3])

		subKey = "%s~%s" % (pType, polarity)

		if cachedRepoHash.has_key(row[0]):
			cachedRepoHash[id][subKey] = count
		else:
			cachedRepoHash[id] = { subKey: count }


def get(data):
	id = data[0]
	returnVector = []
	if cachedRepoHash.has_key(id):
		for key in cachedRepoHash[id]:
			returnVector.append("%s %s" % (key, cachedRepoHash[id][key]))

	return " ".join(returnVector)