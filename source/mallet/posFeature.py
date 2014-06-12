import mysql.connector
import config

sql = """
select 
	id,
	POS,
	count(*)
from pos
where pos != 'X'
group by id, POS
"""

geniaSql = """
select 
	id,
	POS,
	count(*)
from GeniaTuple
where pos != 'X'
group by id, POS
"""

cachedRepoHash = {}

def cacheRepoHash(connection, option=1):
	selectCursor = connection.cursor(buffered=True)

	if option == 1:
		selectCursor.execute(sql)
	else:
		selectCursor.execute(geniaSql)

	for row in selectCursor:
		id = int(row[0])
		pos = row[1]
		count = int(row[2])

		output = "%s %s" % (pos, count)

		if cachedRepoHash.has_key(row[0]):
			cachedRepoHash[id].append(output)
		else:
			cachedRepoHash[id] = [ output ]

def get(data):
	id = data[0]

	if cachedRepoHash.has_key(id):
		return " ".join(cachedRepoHash[id])
	return " " 