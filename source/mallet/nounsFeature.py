import mysql.connector
import config

sql = """
select 
	id,
	word,
	pos,
	count(*)
from pos
where pos in ('NN', 'NNS', 'NNP', 'NNPS')
group by id, word, pos
"""

geniaSql = """
select 
	id,
	base,
	pos,
	count(*)
from GeniaTuple
where pos in ('NN', 'NNS', 'NNP', 'NNPS')
group by id, word, pos
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
		word = row[1]
		count = int(row[3])

		output = "%s %s" % (word, count)

		if cachedRepoHash.has_key(row[0]):
			cachedRepoHash[id].append(output)
		else:
			cachedRepoHash[id] = [ output ]

def get(data):
	id = data[0]

	if cachedRepoHash.has_key(id):
		return " ".join(cachedRepoHash[id])
	return " " 