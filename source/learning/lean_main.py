import sys
import imp
import mysql.connector
import classify
import utils
import sqlStatements
import os
import csv
import dataSplit
import dataPreserve

import logging
import numpy as np
from optparse import OptionParser
from time import time
# import pylab as pl

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
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

def extractData(rawData):
	data = []

	for row in rawData:
		data.append(row[1])

	return data


def getClassData(connection, recordClassifiers):
	selectCursor = connection.cursor(buffered=True)
	selectCursor.execute(recordClassifiers)

	repo = {}

	for row in selectCursor:
		id = row[0]
		disease = row[1]
		className = row[3]
		source = row[4]

		if not repo.has_key(source):
			repo[source] = { disease: { id: className } }
		else:
			if not repo[source].has_key(disease):
				repo[source][disease] = { id: className }
			else:
				if not repo[source][disease].has_key(id):
					repo[source][disease][id] = className

	selectCursor.close()

	return repo

def buildTrainAndTestClassifiers(classifierRepo, trainIdDomain, testIdDomain):
	classifiers = {}

	for sourceKey in classifierRepo:
		classifiers[sourceKey] = {}

		for diseaseName in classifierRepo[sourceKey]:
			classifiers[sourceKey][diseaseName] = {}
			trainArray = []
			testArray = []

			for trainId in trainIdDomain:
				if classifierRepo[sourceKey][diseaseName].has_key(trainId):
					trainArray.append(classifierRepo[sourceKey][diseaseName][trainId])
				else:
					trainArray.append(4)

			for testId in testIdDomain:
				if classifierRepo[sourceKey][diseaseName].has_key(testId):
					testArray.append(classifierRepo[sourceKey][diseaseName][testId])
				else:
					testArray.append(4)

			classifiers[sourceKey][diseaseName][test] = np.array(testArray)
			classifiers[sourceKey][diseaseName][train] = np.array(trainArray)

	return classifiers

def main():
	# mysql connection
	cnx = mysql.connector.connect(
							user='admin', 
							password='onetwotree',
							host='192.168.1.5',
							database='patientdischarge')

	trainDataRaw = getData(cnx, (trainFilter,))
	testDataRaw = getData(cnx, (testFilter,))

	trainData = extractData(trainDataRaw[0])
	testData = extractData(testDataRaw[0])

	classifierTuples = getClassData(cnx)
	actualClassifiers = buildTrainAndTestClassifiers(classifierTuples, trainDataRaw[1], testDataRaw[1])

	with open('results.csv', 'wb') as csvfile:
		resultWriter = csv.writer(csvfile)
		resultWriter.writerow(['Source', 'Disease', 'Micro Precision', 'Macro Precision', 'F1-Score'])

		for clf, name in ((LogisticRegression(), "MaxEnt"),):

			for sourceKey in actualClassifiers:

				for diseaseKey in actualClassifiers[sourceKey]:
					print "doing " + sourceKey + " " + diseaseKey

					vectorizer = HashingVectorizer(stop_words='english', non_negative=True,
			                                   n_features=2 ** 16)

					X_train = vectorizer.fit_transform(trainData)
					X_test = vectorizer.transform(testData)

					y_train = actualClassifiers[sourceKey][diseaseKey][train]
					y_test = actualClassifiers[sourceKey][diseaseKey][test]

					clf.fit(X_train, y_train)

					pred = clf.predict(X_test)
					f1Score = metrics.f1_score(y_test, pred)
					macroPrecision = metrics.precision_score(y_test, pred, average="macro")
					microPrecision = metrics.precision_score(y_test, pred, average="micro")
					resultWriter.writerow([name, sourceKey, diseaseKey, microPrecision, macroPrecision, f1Score])
	
if __name__ == '__main__':
	main()