import sys
import imp
import mysql.connector
import classify
import utils
import sqlStatements
import os
import csv
import datetime

import logging
import numpy as np
import scipy.sparse as sp
from scipy.sparse import coo_matrix
from optparse import OptionParser
from time import time
# import pylab as pl

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.utils.extmath import density
from sklearn import metrics

testFilter = "data/test"
trainFilter = "data/train"

train = "train"
test = "test"

textual = "textual"
intuitive = "intuitive"

insertResultTemplate = """
insert into patientdischarge.ClassifierResults(FeatureSelectionName, ClassifierName, DiseaseName, PrecisionResult, RecallResult, FScoreResult, DateUploaded) 
values (%s, %s, %s, %s, %s, %s, %s)
"""

recordClassifiers = """
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

dataTemplateSql = """
select distinct
	ID,
	Text,
	Type
from patientdischarge.patientdischargesummaries
where Type = %s
order by ID asc
"""

sentimentSql = """
select 
	id,
	type,
	priorpolarity,
	count(*)
from SubjectiveLexicon sl
join historywordposnormalized hwpn
	on sl.pos = hwpn.posnormalized and sl.word = hwpn.word
group by id, type, priorpolarity, posnormalized
order by id
"""

def getData(connection, tup):
	selectCursor = connection.cursor(buffered=True)
	selectCursor.execute(dataTemplateSql, tup)

	list_data = []
	domainIds = []

	for row in selectCursor:
		list_data.append(row[0:])
		domainIds.append(row[0])

	selectCursor.close()

	return (list_data, domainIds)

def getAndBuildSentiment(connection, trainDomain, testDomain):
	# expecting vectors of [positive, posCount, negative, negCount, neutral, neutralCount, both, bothCount]
	# build the hash
	selectCursor = connection.cursor(buffered=True)
	selectCursor.execute(sentimentSql)

	returnHash = {}
	typeHash = { "weaksubj": 1, "strongsubj": 2 }
	polarityHash = { "positive": 1, "negative": 2, "neutral": 3, "both": 4 }

	for row in selectCursor:
		id = int(row[0])
		sType = row[1]
		sentiment = row[2]
		count = int(row[3])

		if not returnHash.has_key(id):
			returnHash[id] = {}
			returnHash[id][(sType, sentiment)] = count
		else: 
			returnHash[id][(sType, sentiment)] = count

	trainVector = []
	for id in trainDomain:
		tempList = []

		for typeKey in typeHash:
			sType = typeHash[typeKey]

			for polarityKey in polarityHash:
				sentiment = polarityHash[polarityKey]

				tempList.append(sType)
				tempList.append(sentiment)

				tup = (sType, sentiment)
				if returnHash.has_key(id) and returnHash[id].has_key(tup):
					tempList.append(returnHash[id][tup])
				else:
					tempList.append(0)

		trainVector.append(tempList)

	testVector = []
	for id in testDomain:
		tempList = []

		for typeKey in typeHash:
			sType = typeHash[typeKey]

			for polarityKey in polarityHash:
				sentiment = polarityHash[polarityKey]

				tempList.append(sType)
				tempList.append(sentiment)

				tup = (sType, sentiment)
				if returnHash.has_key(id) and returnHash[id].has_key(tup):
					tempList.append(returnHash[id][tup])
				else:
					tempList.append(0)

		testVector.append(tempList)

	return (trainVector, testVector)

def extractData(rawData):
	data = []

	for row in rawData:
		data.append(row[1])

	return data

def getClassData(connection):
	selectCursor = connection.cursor(buffered=True)
	selectCursor.execute(recordClassifiers)

	repo = {}

	for row in selectCursor:
		id = row[0]
		disease = row[1]
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

def insertClassifierResults(connection, resultTuple):
	cursor = connection.cursor(buffered=True)
	cursor.execute(insertResultTemplate, resultTuple)
	connection.commit()
	print "submitted " + str(resultTuple)

def main():
	# mysql connection
	featureSelectionName = "polarity sentiment, with weak/strong"

	cnx = mysql.connector.connect(
							user='admin', 
							password='onetwotree',
							host='192.168.1.5',
							database='patientdischarge')

	today = datetime.date.today()

	trainDataRaw = getData(cnx, (trainFilter,))
	testDataRaw = getData(cnx, (testFilter,))

	trainData = extractData(trainDataRaw[0])
	testData = extractData(testDataRaw[0])

	sentimentData = getAndBuildSentiment(cnx, trainDataRaw[1], testDataRaw[1])

	X_train_sent_features = coo_matrix(sentimentData[0])
	
	X_test_sent_features = coo_matrix(sentimentData[1])

	classifierTuples = getClassData(cnx)
	actualClassifiers = buildTrainAndTestClassifiers(classifierTuples, trainDataRaw[1], testDataRaw[1])

	for clf, name in (
		(LogisticRegression(), "MaxEnt"),
		(RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
    	(Perceptron(n_iter=50), "Perceptron"),
    	(PassiveAggressiveClassifier(n_iter=50), "Passive-Aggressive"),
		(KNeighborsClassifier(n_neighbors=10), "kNN")):
			for diseaseKey in actualClassifiers:
				print "doing " + " " + diseaseKey + " " + name

				vectorizer = CountVectorizer()

				X_train = vectorizer.fit_transform(trainData)
				X_test = vectorizer.transform(testData)

				X_train_combine = sp.hstack((X_train_sent_features, X_train))
				X_test_combine = sp.hstack((X_test_sent_features, X_test))

				y_train = actualClassifiers[diseaseKey][train]
				y_test = actualClassifiers[diseaseKey][test]

				clf.fit(X_train_combine.A, y_train)

				pred = clf.predict(X_test_combine.A)

				f1Score = metrics.f1_score(y_test, pred, average="none")
				precision = metrics.precision_score(y_test, pred, average="none")
				recall = metrics.recall_score(y_test, pred, average="none")
				insertClassifierResults(cnx, (featureSelectionName, name, diseaseKey, np.float(precision), np.float(recall), np.float(f1Score), today))
	
if __name__ == '__main__':
	main()