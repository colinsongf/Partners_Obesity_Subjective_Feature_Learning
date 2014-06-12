import mysql.connector

recordClassificationSql = """
select 
	distinct ID, Name 
from patientdischarge.recordclassification
order by ID
"""

insertClusterSql = """
insert into patientdischarge.recordclassificationcluster(ID, Cluster)
values (%s, %s)
"""

def insertClusters(connection):
	selectCursor = connection.cursor(buffered=True)

	selectCursor.execute(recordClassificationSql)
	clusterDict = {}
	for (ID, Name) in selectCursor:
		if clusterDict.has_key(ID):
			clusterDict[ID].append(Name)
		else:
			clusterDict[ID] = [Name]
	selectCursor.close()

	insertCursor = connection.cursor(buffered=True)
	for key in clusterDict:
		clusterDict[key].sort()
		cluster = "_".join(clusterDict[key])
		insertCursor.execute(insertClusterSql, (key, cluster))
		connection.commit()
		print "inserted %s %s" % (key, cluster)

	insertCursor.close()