import os
import re
import sys
import shutil
import config
import numpy as np
import getPatientData
import insertResult
import mysql.connector
import subjectiveComplexFeature
import subjectiveSimpleFeature
import subjectiveWordSimpleFeature
import subjectiveWordComplexFeature
import subjectiveDiseaseUniqueFeature
import highestProbabilityFeature
import wordCountFeature
import platform
import readConfusionMatrix
import featureSetup

from sklearn import metrics

train = "train"
test = "test"

baseFolderLocation = "data/mallet"

removeDirCommand = "rmdir %s\data\mallet /s /q"
removeDirUnixCommand = "sudo rm -r %s/data/mallet"

malletImportTrainCommand = "%s/mallet/bin/mallet import-file --output %s/train.vectors --input %s/train.txt"
malletImportTestCommand = "%s/mallet/bin/mallet import-file --output %s/test.vectors --input %s/test.txt --use-pipe-from %s/train.vectors"
malletTrainClassifier = "%s/mallet/bin/mallet train-classifier --training-file %s/train.vectors --testing-file %s/test.vectors --output-classifier %s/me.model --trainer MaxEnt > %s/me.stdout"
malletClassiferInfo = "%s/mallet/bin/mallet classify-info --classifier %s/me.model > %s/me.txt"

def rmdirAndRemakeIfExists(directory):
	if os.path.exists(directory):
		shutil.rmtree(directory)
	os.makedirs(directory)

def mkdirIfNotExists(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def writeTextToDir(data, diseaseKey, classKey, actualClassifiers, diseaseFolder, textFile, features):
	fileStream = open(textFile, "w")

	for i in range(0, len(data)):
		label = str(actualClassifiers[diseaseKey][classKey][i])
		
		fileStream.write("%s %s" % (data[i][0], label))

		for feature in features:
			fileStream.write(" %s" % feature.get(data[i]))

		# each new line is a new instance
		fileStream.write("\n")

	fileStream.close()
		
	
def readAndUploadClassifierOutput(featureSet, diseaseFolder, disease, connection, source):
	text = open(diseaseFolder + "/me.stdout", "r").read()

	(confusionMatrix, confusionLabelDict, y_truth, y_pred, trueCount) = readConfusionMatrix.readText(text)

	precisionMicro = np.float(metrics.precision_score(y_truth, y_pred, average="micro"))
	recallMicro = np.float(metrics.recall_score(y_truth, y_pred, average="micro"))
	f1Micro = np.float(metrics.f1_score(y_truth, y_pred, average="micro"))
	f1Macro = np.float(metrics.f1_score(y_truth, y_pred, average="macro"))
	precisionMacro = np.float(metrics.precision_score(y_truth, y_pred, average="macro"))
	recallMacro = np.float(metrics.recall_score(y_truth, y_pred, average="macro"))
	accuracy = np.float(metrics.accuracy_score(y_truth, y_pred))

	insertResult.insertClassifierResults(connection, (featureSet, "maxent", trueCount, disease, precisionMicro, recallMicro, f1Micro, recallMacro, precisionMacro, f1Macro, source, accuracy))

def calculateAggregateResults(connection, featureSet, source):
	cursor = connection.cursor(buffered=True)

	sqlTemplate = "select featureselectionname, diseasename, microprecision, microrecall, microf1score, macrorecall, macroprecision, macrof1score, accuracy from classifierresults where featureselectionname = %s and source = %s"
	cursor.execute(sqlTemplate, (featureSet, source))

	microPrecision = []
	microRecall = []
	microf1 = []
	recall = []
	precision = []
	macrof1 = []
	accuracy = []

	total = 0
	for row in cursor:
		total = total + 1
		diseaseName = row[1]
		microPrecision.append(float(row[2]))
		microRecall.append(float(row[3]))
		microf1.append(float(row[3]))

		recall.append(float(row[4]))
		precision.append(float(row[5]))
		macrof1.append(float(row[6]))

		accuracy.append(float(row[7]))

	total = float(total)

	cursor.close()

	insertResult.insertAggregateResults(connection, 
		(np.float(np.mean(microPrecision)), 
			np.float(np.mean(microRecall)), 
			np.float(np.mean(microf1)), 
			np.float(np.mean(recall)), 
			np.float(np.mean(precision)), 
			np.float(np.mean(macrof1)), 
			featureSet, 
			source,
			np.float(np.mean(accuracy))))

def main():
	# get arguments from command line
	# define features to use
	source = sys.argv[1]
	featureArg = sys.argv[2]

	# setup features
	if not featureSetup.features.has_key(featureArg):
		print "count not find feature %s" % (featureArg,)

	featureSet = featureSetup.featureDesc[featureArg]
	features = featureSetup.features[featureArg]()

	# get data
	(trainData, testData, actualClassifiers) = getPatientData.getDataAndClassifiers(config.connection, (source,))

	# transform the data
	for diseaseKey in actualClassifiers:
		diseaseFolder = "%s/%s" % (baseFolderLocation, diseaseKey)

		trainTextFile = "%s/train.txt" % (diseaseFolder,)
		testTextFile = "%s/test.txt" % (diseaseFolder,)
		
		rmdirAndRemakeIfExists(diseaseFolder)

		writeTextToDir(trainData, diseaseKey, train, actualClassifiers, diseaseFolder, trainTextFile, features)
		writeTextToDir(testData, diseaseKey, test, actualClassifiers, diseaseFolder, testTextFile, features)

		os.system(malletImportTrainCommand % (os.getcwd(), diseaseFolder, diseaseFolder))
		os.system(malletImportTestCommand % (os.getcwd(), diseaseFolder, diseaseFolder, diseaseFolder))
		os.system(malletTrainClassifier % (os.getcwd(), diseaseFolder, diseaseFolder, diseaseFolder, diseaseFolder))
		os.system(malletClassiferInfo % (os.getcwd(), diseaseFolder, diseaseFolder))

		readAndUploadClassifierOutput(featureSet, diseaseFolder, diseaseKey, config.connection, source)
	
	calculateAggregateResults(config.connection, featureSet, source)

if __name__ == '__main__':
	main()