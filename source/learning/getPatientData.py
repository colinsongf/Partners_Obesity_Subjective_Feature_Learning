import mysql.connector
import numpy as np
import re

emptystring = ""
whitespace = "\\s+"
train = "train"
test = "test"

testFilter = "data/test"
trainFilter = "data/train"

dataTemplateSql = """
select distinct
	ID,
	Text,
	Type
from patientdischarge.patientdischargesummaries
where Type = %s
order by ID asc
"""

recordClassifierSql = """
select distinct 
	rc.ID,
	rc.Name,
	dcs.Type,
	case rc.Class
		when 'Y' then 1
		when 'N' then 2
		when 'Q' then 3
		when 'U' then 4
	end as Class,
	rc.Source
from patientdischarge.RecordClassification rc
join patientdischarge.patientdischargesummaries dcs
	on rc.ID = dcs.ID
order by ID asc
"""

def getTrainData(connection):
	selectCursor = connection.cursor(buffered=True)
	selectCursor.execute(dataTemplateSql, (trainFilter,))

	list_data = []
	domainIds = []

	for row in selectCursor:
		list_data.append(row[0:])
		domainIds.append(row[0])

	selectCursor.close()

	return (list_data, domainIds)

def getTestData(connection):
	selectCursor = connection.cursor(buffered=True)
	selectCursor.execute(dataTemplateSql, (testFilter,))

	list_data = []
	domainIds = []

	for row in selectCursor:
		list_data.append(row[0:])
		domainIds.append(row[0])

	selectCursor.close()

	return (list_data, domainIds)

def extractData(rawData):
	data = []

	for row in rawData:
		data.append(row[1])

	return data

def getClassData(connection):
	selectCursor = connection.cursor(buffered=True)
	selectCursor.execute(recordClassifierSql)

	repo = {}

	for row in selectCursor:
		id = row[0]
		disease = re.sub(whitespace, emptystring, row[1])
		className = row[3]
		source = row[4]

		if not repo.has_key(disease):
			repo[disease] = {}

		if className == 1:
			repo[disease][id] = None

	selectCursor.close()

	return repo

def buildTrainAndTestClassifiers(classifierRepo, trainIdDomain, testIdDomain):
	classifiers = {}

	for diseaseName in classifierRepo:
		classifiers[diseaseName] = {}

		trainArray = []
		testArray = []

		for trainId in trainIdDomain:
			if classifierRepo[diseaseName].has_key(trainId):
				trainArray.append(1)
			else:
				trainArray.append(2)

		for testId in testIdDomain:
			if classifierRepo[diseaseName].has_key(testId):
				testArray.append(1)
			else:
				testArray.append(2)
		
		classifiers[diseaseName][test] = np.array(testArray)
		classifiers[diseaseName][train] = np.array(trainArray)

	return classifiers

def getDataAndClassifiers(connection):
	trainDataRaw = getTrainData(connection)
	testDataRaw = getTestData(connection)

	trainData = extractData(trainDataRaw[0])
	testData = extractData(testDataRaw[0])

	classifierTuples = getClassData(connection)
	actualClassifiers = buildTrainAndTestClassifiers(classifierTuples, trainDataRaw[1], testDataRaw[1])

	return (trainData, testData, actualClassifiers)

