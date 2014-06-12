import os
import re
import shutil
import config
import numpy as np
import getPatientData
import insertResult
import mysql.connector

train = "train"
test = "test"

baseFolderLocation = "data/mallet"

removeDirCommand = "rmdir " + baseFolderLocation

malletImportTrainCommand = "%s/mallet/bin/mallet import-dir --output %s/train.vectors --gram-sizes %s --remove-stopwords --input %s %s"
malletImportTestCommand = "%s/mallet/bin/mallet import-dir --output %s/test.vectors --gram-sizes %s --remove-stopwords --input %s %s --use-pipe-from %s/train.vectors"
malletTrainClassifier = "%s/mallet/bin/mallet train-classifier --training-file %s/train.vectors --testing-file %s/test.vectors --output-classifier %s/me.model --trainer MaxEnt > %s/me.stdout"
malletClassiferInfo = "%s/mallet/bin/mallet classify-info --classifier %s/me.model > %s/me.txt"

def rmdirAndRemakeIfExists(directory):
	if os.path.exists(directory):
		shutil.rmtree(directory)
	os.makedirs(directory)

def mkdirIfNotExists(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def writeTextToDir(data, diseaseKey, classKey, actualClassifiers, diseaseFolder):
	folders = {}
	for i in range(0, len(data)):
		folder = str(actualClassifiers[diseaseKey][classKey][i])
		text = data[i]

		mkdirIfNotExists(folder)

		immediateFolder = "%s/%s/%s" % (diseaseFolder, classKey, folder)

		folders[immediateFolder] = None
		
		mkdirIfNotExists(immediateFolder)
		
		filePath = "%s/%s" % (immediateFolder, i)
		
		stream = open(filePath, "w")
		stream.write(text)

	for key in folders:
		yield key
	
def readAndUploadClassifierOutput(diseaseFolder, disease, connection):
	lines = open(diseaseFolder + "/me.stdout", "r").read().split("\n")

	numberRegex = "0[\.][0-9]+"

	startIdx = 22
	metaInfo = { 
		22: "accuracy" ,
		23: "precision" ,
		24: "precision" ,
		25: "recall" ,
		26: "recall" ,
		27: "f1" ,
		28: "f1"
	}

	storage = {}

	for key in metaInfo:
		match = re.search(numberRegex, lines[key])

		if match is not None:
			val = float(lines[key][match.start():match.end()])

			if storage.has_key(metaInfo[key]):
				existingVal = storage[metaInfo[key]]

				newVal = (existingVal + val) / float(2)
				storage[metaInfo[key]] = newVal
			else:
				storage[metaInfo[key]] = val

	insertResult.insertClassifierResults(connection, ("mallet baseline", "maxent", 0, disease, 0, np.float(storage["recall"]), np.float(storage["precision"]), np.float(storage["f1"])))

	print storage

def main():
	# get data
	(trainData, testData, actualClassifiers) = getPatientData.getDataAndClassifiers(config.connection)
	
	os.system(removeDirCommand)
	os.mkdir(baseFolderLocation)

	for diseaseKey in actualClassifiers:
		diseaseFolder = "%s/%s" % (baseFolderLocation, diseaseKey)
		print "writing files for %s " % (diseaseFolder,)

		rmdirAndRemakeIfExists(diseaseFolder)

		trainFolders = list(writeTextToDir(trainData, diseaseKey, train, actualClassifiers, diseaseFolder))
		testFolders = list(writeTextToDir(testData, diseaseKey, test, actualClassifiers, diseaseFolder))

		os.system(malletImportTrainCommand % (os.getcwd(), diseaseFolder, 1, trainFolders[0], trainFolders[1]))
		os.system(malletImportTestCommand % (os.getcwd(), diseaseFolder, 1, testFolders[0], testFolders[1], diseaseFolder))
		os.system(malletTrainClassifier % (os.getcwd(), diseaseFolder, diseaseFolder, diseaseFolder, diseaseFolder))
		os.system(malletClassiferInfo % (os.getcwd(), diseaseFolder, diseaseFolder))
		readAndUploadClassifierOutput(diseaseFolder, diseaseKey, config.connection)

if __name__ == '__main__':
	main()