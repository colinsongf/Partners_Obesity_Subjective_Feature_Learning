import mysql.connector
import config

baseNameEntity = """
SELECT 
	ID,
	NamedEntity,
	Count(*)
FROM patientdischarge.GeniaTuple
where id = %s
group by id, namedentity
"""

cachedCon = config.connection
def cacheRepoHash(connection):
	cachedCon = connection

def get(data):
	id = data[0]

	cursor = cachedCon.cursor(buffered=True)

	cursor.execute(baseNameEntity, (id,))

	returnVector = []
	for row in cursor:
		namedEntity = row[1]
		count = row[2]

		returnVector.append(" %s %s" % (namedEntity, count))

	return " ".join(returnVector)