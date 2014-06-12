import mysql.connector
import config

baseNameEntity = """
select 
	ID,
	Chunk,
	count(*)
from
(
select
	ID,
	case 
		when chunk like '%%ADJP%%' then 'ADJP'
		when chunk like '%%ADVP%%' then 'ADVP'
		when chunk like '%%CONJP%%' then 'CONJP'
		when chunk like '%%INTJ%%' then 'INTJ'
		when chunk like '%%LST%%' then 'LST'
		when chunk like '%%NP%%' then 'NP'
		when chunk like '%%PP%%' then 'PP'
		when chunk like '%%PRT%%' then 'PRT'
		when chunk like '%%SBAR%%' then 'SBAR'
		when chunk like '%%VP%%' then 'VP'
		when chunk like 'O' then 'O'
	end as Chunk
from geniatuple
where id = %s
) b
group by ID, Chunk
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
		chunk = row[1]
		count = row[2]

		returnVector.append(" %s %s" % (chunk, count))

	return " ".join(returnVector)