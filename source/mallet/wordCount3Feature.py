import mysql.connector
import config

sql = """
select 
	id,
	pos,
	word,
	count(*)
from pos
where pos not in ('X', '-LRB-', '-RBR-', '-RRB-', '.', ':', ',') and id = %s
group by id, pos, word
"""

cachedRepoHash = {}
cachedConnection = config.connection
def cacheRepoHash(connection):
	pass

def get(data):
	id = data[0]

	selectCursor = cachedConnection.cursor(buffered=True)
	selectCursor.execute(sql, (id,))

	returnArray = []

	for row in selectCursor:
		word = row[2]
		count = row[3]

		returnArray.append("%s %s" % (word, count))

	selectCursor.close()
	return " ".join(returnArray)