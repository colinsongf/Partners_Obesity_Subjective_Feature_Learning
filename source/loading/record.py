import mysql.connector
import xml.etree.ElementTree as ET
import json
import os
from os import listdir

recordDocQuery = ".//doc"
diseasesQuery = ".//diseases"

maxInsertCount = 1000

recordInsertStatement = ("insert into patientdischarge.patientdischargesummaries (ID, Text, Type) "
				"values (%s, %s, %s)")

unigramInsertStatement = ("insert into patientdischarge.unigrams (ID, Word, Prob) " 
							"values (%s, %s, %s)")

bigramInsertStatement = ("insert into patientdischarge.bigrams (ID, Word, PrevWord, Prob) " 
							"values (%s, %s, %s, %s)")

trigramInsertStatement = ("insert into patientdischarge.trigrams (ID, Word, PrevWord, PrevPrevWord, Prob) " 
							"values (%s, %s, %s, %s, %s)")

def insertNgrams(folder, connection):
	cur = connection.cursor(buffered=True)

	count = 0
	totalCount = 500

	fileCount = 0
	totalFiles = len([name for name in os.listdir(folder) if os.path.isfile(name)])

	for fileName in listdir(folder):
		fileCount = fileCount + 1

		print "%s/%s files..." % (fileCount, totalFiles)

		recordFile = open(folder + "/" + fileName).read()
		data = json.loads(recordFile)

		id = data["id"]

		
		for unigram in data["uni"]:

			valueTuple = (id, unigram, data["uni"][unigram])
			cur.execute(unigramInsertStatement, valueTuple)
			
			if count > totalCount:
				print 'unigram ' + str(id)
				count = 0
				connection.commit()

			count = count + 1
					
		for bigram in data["bi"]:
			
			bigramDict = data["bi"][bigram]

			for subkey in bigramDict:
				valueTuple = (id, bigram, subkey, bigramDict[subkey])
				cur.execute(bigramInsertStatement, valueTuple)
				
				if count > totalCount:
					print 'bigram ' + str(id)
					count = 0
					connection.commit()

				count = count + 1

		for trigram in data["tri"]:

			trigramDict = data["tri"][trigram]

			for subkey in trigramDict:
				subkeys = subkey.split("~")

				valueTuple = (id, trigram, subkeys[0], subkeys[1], trigramDict[subkey])
				cur.execute(trigramInsertStatement, valueTuple)
				if count > totalCount:
					print 'trigram ' + str(id)
					count = 0
					connection.commit()

				count = count = 1

		connection.commit()
		count = 0

def insertRecords(folders, connection):
	cur = connection.cursor(buffered=True)
	
	# patient records
	for recordFolder in folders:

		for fileName in listdir(recordFolder):
			# read in entire file
			tree = ET.parse(recordFolder + "/" + fileName)

			# get and parse
			root = tree.getroot()

			for element in root.findall(recordDocQuery):
				
				valueTuple = (element.attrib["id"], element[0].text, recordFolder)
				cur.execute(recordInsertStatement, valueTuple)
				connection.commit()
				
				print "uploaded " + valueTuple[0]

def insertAnnotations(recordFolder, connection):
	cur = connection.cursor(buffered=True)
	valuesDict = {}
	for fileName in listdir(recordFolder):
		
		tree = ET.parse(recordFolder + "/" + fileName)
		root = tree.getroot()
		

		for element in root.findall(diseasesQuery):
			diseaseSource = element.attrib["source"].strip()
			for elementSource in element:
				diseaseName = elementSource.attrib["name"].strip()
				for docSource in elementSource:
					diseaseId = docSource.attrib["id"].strip()
					judgment = docSource.attrib["judgment"].strip()
					valueTuple = (diseaseId, diseaseName, diseaseSource, judgment)
					key = "%s~%s~%s~%s" % valueTuple

					if not valuesDict.has_key(key):
						valuesDict[key] = valueTuple

	template = "insert into patientdischarge.recordclassification "
	sqlStrBuilder = template
	insertCount = 0

	for key in valuesDict:
		if insertCount % maxInsertCount == 0:
			sqlStrBuilder = sqlStrBuilder + "\nselect %s, '%s', '%s', '%s'" % valuesDict[key]
			cur.execute(sqlStrBuilder)
			connection.commit()
			print 'committed ' + str(insertCount)
			sqlStrBuilder = template
		else:
			sqlStrBuilder = sqlStrBuilder + "\nselect %s, '%s', '%s', '%s'\nunion" % valuesDict[key]

		insertCount = insertCount + 1
	
	if insertCount % maxInsertCount != 0:
		sqlStrBuilder = sqlStrBuilder + "\nselect %s, '%s', '%s', '%s'" % (0, 'remove', 'remove', 'remove')
		cur.execute(sqlStrBuilder)
		connection.commit()
		sqlStrBuilder = template
		print 'committed ' + str(insertCount)