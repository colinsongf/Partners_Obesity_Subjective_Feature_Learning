import sys
import imp
import mysql.connector
import classify
import utils
import sqlStatements
import os
import csv
import datetime
import getPatientData
import config
import insertResult

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
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.utils.extmath import density
from sklearn import metrics

train = "train"
test = "test"

textual = "textual"
intuitive = "intuitive"

def main():
	# mysql connection
	featureSelectionName = "baseline"

	# get data
	(trainData, testData, actualClassifiers) = getPatientData.getDataAndClassifiers(config.connection)

	# for aggregate scores
	allMicrosF1Scores = []
	allF1scores = []
	allPrecisions = []
	allRecalls = []

	# just using maxent
	for clf, name in ((SGDClassifier(), "SGD"),):
		for diseaseKey in actualClassifiers:
			print "doing " + " " + diseaseKey + " " + name

			vectorizer = CountVectorizer()

			X_train = vectorizer.fit_transform(trainData)
			X_test = vectorizer.transform(testData)

			y_train = actualClassifiers[diseaseKey][train]
			y_test = actualClassifiers[diseaseKey][test]

			clf.fit(X_train, y_train)

			pred = clf.predict(X_test)

			count = 0
			for item in pred:
				if item == 1:
					count = count + 1

			microf1Score = metrics.f1_score(y_test, pred, average="micro")
			f1Score = metrics.f1_score(y_test, pred, average="macro")
			precision = metrics.precision_score(y_test, pred, average="macro")
			recall = metrics.recall_score(y_test, pred, average="macro")

			allMicrosF1Scores.append(microf1Score)
			allF1scores.append(f1Score)
			allPrecisions.append(precision)
			allRecalls.append(recall)

			insertResult.insertClassifierResults(config.connection, (featureSelectionName, name, count, diseaseKey, np.float(microf1Score), np.float(recall), np.float(precision), np.float(f1Score)))

	microF1 = np.array(allMicrosF1Scores)
	macroRecall = np.array(allRecalls)
	macroPrecision = np.array(allPrecisions)
	macroF1 = np.array(allF1scores)
	
	tup = (np.float(np.mean(microF1)), np.float(np.mean(macroRecall)), np.float(np.mean(macroPrecision)), np.float(np.mean(macroF1)), "average")
	insertResult.insertAggregateResults(config.connection, tup)

	tup1 = (np.float(np.std(microF1)), np.float(np.std(macroRecall)), np.float(np.std(macroPrecision)), np.float(np.std(macroF1)), "std")
	insertResult.insertAggregateResults(config.connection, tup1)

if __name__ == '__main__':
	main()