import mysql.connector
import xml.etree.ElementTree as ET
import json
import re
from os import listdir

recordDocQuery = ".//doc"
diseasesQuery = ".//diseases"

whiteSpaceRegex = "[\s]+"

maxInsertCount = 1000

recordInsertStatement = ("insert into patientdischarge.patientdischargesummariescleansed (ID, Text, Type, Class) "
				"values (%s, %s, %s, %s)")

unigramInsertStatement = ("insert into patientdischarge.unigrams (ID, Word, Prob) " 
							"values (%s, %s, %s)")

bigramInsertStatement = ("insert into patientdischarge.bigrams (ID, Word, PrevWord, Prob) " 
							"values (%s, %s, %s, %s)")

trigramInsertStatement = ("insert into patientdischarge.trigrams (ID, Word, PrevWord, PrevPrevWord, Prob) " 
							"values (%s, %s, %s, %s, %s)")

def insertNgrams(folder, connection):
	cur = connection.cursor(buffered=True)

	for fileName in listdir(folder):
		recordFile = open(folder + "/" + fileName).read()
		data = json.loads(recordFile)

		id = data["id"]

		i = 0
		
		for unigram in data["uni"]:

			valueTuple = (id, unigram, data["uni"][unigram])
			cur.execute(unigramInsertStatement, valueTuple)

			print valueTuple
			i = i + 1
			if i % 100 == 0:
				connection.commit()
				
		i = 0	
		for bigram in data["bi"]:
			
			bigramDict = data["bi"][bigram]

			for subkey in bigramDict:
				valueTuple = (id, bigram, subkey, bigramDict[subkey])
				cur.execute(bigramInsertStatement, valueTuple)

				print valueTuple

			i = i + 1
			if i % 100 == 0:
				connection.commit()

		i = 0
		for trigram in data["tri"]:

			trigramDict = data["tri"][trigram]

			for subkey in trigramDict:
				subkeys = subkey.split("~")

				valueTuple = (id, trigram, subkeys[0], subkeys[1], trigramDict[subkey])
				cur.execute(trigramInsertStatement, valueTuple)

				print valueTuple

			i = i + 1
			if i % 100 == 0:
				connection.commit()

		connection.commit()

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
				valueTuple = (element.attrib["id"], reconstruct(element[0].text), recordFolder)

				cur.execute(recordInsertStatement, valueTuple)
				connection.commit()
				
				print "uploaded " + valueTuple[0]

def reconstruct(text):
	obeseRegex = "obes(?i)"
	obeseReplace = "#obese#"

	asthmaRegex = "asthm(?i)"
	asthmaReplace = "#asthma#"

	normalizedText = re.sub(whiteSpaceRegex, " ", text)

	words = []
	for word in normalizedText.split(" "):
		if re.search(obeseRegex, word):
			words.append(obeseReplace)
		elif re.search(asthmaRegex, word):
			words.append(asthmaReplace)
		else:
			words.append(word)

	return " ".join(words)