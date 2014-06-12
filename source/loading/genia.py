import os
import json
import nltk

parsedSentencesProperty = "ParsedSentences"

fileTemplate = "%s/%s"

geniaTag = "./geniatagger < %s > %s"

insertGeniaTagSql = """
insert into GeniaTuple(ID, Word, Base, Pos, Chunk, NamedEntity) 
values(%s, %s, %s, %s, %s, %s)
"""

def outputGeniaTag(inputFolder, intermediateFolder, outputFolder):
	for jsonFile in os.listdir(inputFolder):
		if not jsonFile.isdigit():
			continue
		
		fileLocation = fileTemplate % (inputFolder, jsonFile)
		print fileLocation
		strData = open(fileLocation).read()
		
		jsonData = None
		try:
			jsonData = json.loads(strData)
		except ValueError:
			print "error with " + str(jsonFile)
			continue

		fStream = open(fileTemplate % (intermediateFolder, jsonFile), "w")
		for parsedSentence in jsonData[parsedSentencesProperty]:
			fStream.write(parsedSentence.encode('ascii', 'ignore'))
			fStream.write("\n")

	for fileName in os.listdir(intermediateFolder):
		outputFile = fileTemplate % (outputFolder, fileName)
		intermediateFile = fileTemplate % (intermediateFolder, fileName)
		os.system(geniaTag % (intermediateFile, outputFile))

def insertGeniaTag(outputFolder, connection):
	cursor = connection.cursor(buffered=True)

	for id in os.listdir(outputFolder):
		actualFile = fileTemplate % (outputFolder, id)

		fStream = open(actualFile)

		line = fStream.readline()
		count = 0
		while line:
			count = count + 1
			items = line.strip().split("\t")
			# print len(items)
			if len(items) == 5:
				word = items[0]
				base = items[1]
				pos = items[2]
				chunk = items[3]
				namedEntity = items[4]
				insertTuple = (id, word, base, pos, chunk, namedEntity)
				# print insertTuple
				cursor.execute(insertGeniaTagSql, insertTuple)

			line = fStream.readline()

		print "saving " + str(count)
		connection.commit()
