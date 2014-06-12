import os
import json
import nltk

fileTemplate = "%s/%s"
parsedSentencesProperty = "ParsedSentences"

insertSentenceTemplate = ("insert into patientdischarge.sentence (ID, SentenceID, Sentence)"
						"values (%s, %s, %s)")

insertPosTemplate = ("insert into patientdischarge.pos (ID, SentenceID, Word, POS, POSConverted)"
					"values (%s, %s, %s, %s, %s)")

latestFile = "1"

subjectiveConvert = {
	"JJ": "adj",
	"JJR": "adj",
	"JJS": "adj",
	"RB": "adverb",
	"RBR": "adverb",
	"RBS": "adverb",
	"NN": "noun",
	"NNS": "adverb",
	"NNP": "adverb",
	"NNPS": "adverb",
	"VBG": "verb",
	"VBD": "verb",
	"VB": "verb",
	"VBN": "verb",
	"VBP": "verb",
	"VBZ": "verb",
}

def insertPos(connection, dataFolder):
	cursor = connection.cursor(buffered=True)

	sentenceId = 0
	processedLatestFile = False

	for jsonFile in os.listdir(dataFolder):
		if jsonFile == latestFile:
			print "skipping " + jsonFile
			processedLatestFile = True

		if not jsonFile.isdigit() or not processedLatestFile:
			continue
		
		fileLocation = fileTemplate % (dataFolder, jsonFile)
		print fileLocation
		strData = open(fileLocation).read()
		
		jsonData = None

		try:
			jsonData = json.loads(strData)
		except ValueError:
			print "error with " + str(jsonFile)
			continue

		id = jsonFile

		for parsedSentence in jsonData[parsedSentencesProperty]:
			sentenceId = sentenceId + 1
			# this is a string
			tree = nltk.Tree(parsedSentence)
			insertTuple = (id, sentenceId, unicode(tree).encode('ascii', 'ignore'))
			cursor.execute(insertSentenceTemplate, insertTuple)
			
			print insertTuple

			for posTuple in tree.pos():

				word = posTuple[0].encode('ascii', 'ignore')
				pos = posTuple[1].encode('ascii', 'ignore')
				posConvert = "none"

				if subjectiveConvert.has_key(pos):
					posConvert = subjectiveConvert[pos]

				insertTuple = (id, sentenceId, word, pos, posConvert)
				cursor.execute(insertPosTemplate, insertTuple)

				print insertTuple
		
		connection.commit()