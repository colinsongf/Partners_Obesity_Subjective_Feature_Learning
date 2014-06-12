import sys
import imp
import mysql.connector
import os
import csv

classificationResultsSql = """
select 
	DiseaseName,
	FeatureSelectionName,
	FScoreResult,
	Classifiername
from classifierresults
order by diseasename, featureselectionname, classifiername
"""

insertClassificationAnalysis = """
insert into classifieranalysis (DiseaseName, FeatureSelectionName, HighestClassifier, LowestClassifier, HighestFScore, LowestFScore, MeanFScore) 
values (%s, %s, %s, %s, %s, %s, %s)
"""

def getData(connection):
	selectCursor = connection.cursor(buffered=True)
	selectCursor.execute(classificationResultsSql)

	for row in selectCursor:
		yield row[0:]

	selectCursor.close()

def insertData(connection, tup):
	insertCursor = connection.cursor(buffered=True)
	insertCursor.execute(insertClassificationAnalysis, tup)
	connection.commit()
	insertCursor.close()

def main():
	# mysql connection
	cnx = mysql.connector.connect(
							user='admin', 
							password='onetwotree',
							host='192.168.1.5',
							database='patientdischarge')

	# build hash with grouped entities together
	groupedEntities = {}

	for record in getData(cnx):
		disease = record[0]
		feature = record[1]
		fscore = float(record[2])
		classifier = record[3]

		tupKey = (disease, feature)
		if groupedEntities.has_key(tupKey):
			groupedEntities[tupKey][classifier] = fscore
		else:
			groupedEntities[tupKey] = { classifier: fscore } 

	# go through each one and calculate highest fscore, lowest fscore, mean fscore
	for key in groupedEntities:
		highestFScore = -999
		lowestFScore = 999

		highestClassifier = None
		lowestClassifier = None

		runningTotal = 0

		for classifierKey in groupedEntities[key]:
			score = groupedEntities[key][classifierKey]
			runningTotal = runningTotal + score

			if score > highestFScore:
				highestClassifier = classifierKey
				highestFScore = score

			if score < lowestFScore:
				lowestClassifier = classifierKey
				lowestFScore = score

			
		meanFScore = float(runningTotal) / len(groupedEntities[key])

		insertTuple = (key[0], key[1], highestClassifier, lowestClassifier, highestFScore, lowestFScore, meanFScore)
		insertData(cnx, insertTuple)

if __name__ == '__main__':
	main()