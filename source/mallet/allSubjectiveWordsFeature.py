import mysql.connector
import config

subjectiveWordSql = """
select 
	distinct
	hw.Word,
	case 
		when sl.Type is null then 'none'
		else sl.Type
	end Type,
	case 
		when sl.PriorPolarity is null then 'none'
		else sl.PriorPolarity
	end Polarity
from SubjectiveLexicon sl
right outer join Pos hw
	on sl.Word = hw.Word and sl.Pos = hw.PosConverted
where hw.ID = %s
"""

cachedCon = config.connection
def cacheRepoHash(connection):
	cachedCon = connection

def get(data):
	id = data[0]

	cursor = cachedCon.cursor(buffered=True)

	cursor.execute(subjectiveWordSql, (id,))

	returnVector = []
	for row in cursor:
		word = row[0]
		pType = row[1]
		polarity = row[2]

		returnVector.append(" %s %s_%s" % (word, pType, polarity))

	return " ".join(returnVector)