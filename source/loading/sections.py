import re
import os
import json
import nltk
import xml.etree.ElementTree as ET

startRegex = " ILLNESS| COURSE| ADMISSION"
endRegex = "[A-Z]*[\s]*[A-Z]{2,}:"

fileTemplate = "%s/%s"

parsedSentencesProperty = "ParsedSentences"

whiteSpaceRegex = "[\s]+"

recordDocQuery = ".//doc"

javaCommand = "cat %s | java -jar %s %s %s"

insertSummaryCommand = ("insert into patientdischarge.historyofillnesssummaries(ID, Text) "
						"values(%s, %s)")

insertSentenceCommand = ("insert into patientdischarge.historysentencepos(ID, SentenceID, Tree) "
						"values(%s, %s, %s)")

insertWordPosCommand = ("insert into patientdischarge.historywordpos(ID, SentenceID, Word, Pos) "
						"values(%s, %s, %s, %s)")

def saveSections(inputFolders, outputFolder):
	numberOfBlank = 0
	keyFile = open("keyFile.txt", "w")

	for inputFolder in inputFolders:

		for fileName in os.listdir(inputFolder):
			if fileName == ".DS_Store":
				continue

			# read in entire file
			tree = ET.parse(inputFolder + "/" + fileName)

			# get and parse
			root = tree.getroot()

			for element in root.findall(recordDocQuery):
				normalizedText = re.sub(whiteSpaceRegex, " ", element[0].text)

				firstIndex = re.search(startRegex, normalizedText)

				if firstIndex == None:
					numberOfBlank = numberOfBlank + 1
					continue

				startIndex = firstIndex.end()

				subStr = normalizedText[startIndex:]

				secondIndex = re.search(endRegex, subStr)

				snippet = subStr
				if not secondIndex == None:
					snippet = subStr[0:secondIndex.start()-1]

				if snippet == "":
					numberOfBlank = numberOfBlank + 1

				writeFile = open("%s/%s" % (outputFolder, element.attrib["id"]), "w")
				writeFile.write(snippet)
				writeFile.close()

				keyFile.write(element.attrib["id"])
				keyFile.write("\n")

	print numberOfBlank

def sectionPosConvert(jarFileLocation, fileLocation, inputFolder, outputFolder):
	print "executing java file for everything..."
	res = os.system(javaCommand % (fileLocation, jarFileLocation, inputFolder, outputFolder))
	print res

def insertSections(connection, folder):
	selectCursor = connection.cursor(buffered=True)

	for fileName in os.listdir(folder):
		text = open(folder + "/" + fileName).read()

		selectCursor.execute(insertSummaryCommand, (fileName, text))
		connection.commit()

def insertSentences(connection, dataFolder):
	cursor = connection.cursor(buffered=True)

	sentenceId = 0
	processedLatestFile = True

	for jsonFile in os.listdir(dataFolder):
		if not jsonFile.isdigit() or not processedLatestFile:
			continue
		
		fileLocation = fileTemplate % (dataFolder, jsonFile)
		print fileLocation
		strData = open(fileLocation).read()
		print strData
		jsonData = json.loads(strData)

		id = jsonFile

		for parsedSentence in jsonData[parsedSentencesProperty]:
			sentenceId = sentenceId + 1
			# this is a string
			tree = nltk.Tree(parsedSentence)

			insertTuple = (id, sentenceId, unicode(tree).encode('ascii', 'ignore'))
			cursor.execute(insertSentenceCommand, insertTuple)
			
			print insertTuple

			for posTuple in tree.pos():
				insertTuple = (id, sentenceId, posTuple[0].encode('ascii', 'ignore'), posTuple[1].encode('ascii', 'ignore'))
				cursor.execute(insertWordPosCommand, insertTuple)

				print insertTuple

		connection.commit()
