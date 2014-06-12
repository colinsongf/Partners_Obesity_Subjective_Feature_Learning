import json
from os import listdir
import xml.etree.ElementTree as ET
import re
import cleansedRecords

# expecting to be executed from root folder
obesityTrainingFolder = "data/train"
obesityTestFolder = "data/test"
obesityAnnotationFolder = "data/annotations"

outputFolder = "data/json"

recordDocQuery = ".//doc"

def main():
	# patient records
	for recordFolder in [obesityTrainingFolder, obesityTestFolder]:
		for fileName in listdir(recordFolder):
			# read in entire file
			tree = ET.parse(recordFolder + "/" + fileName)

			# get and parse
			root = tree.getroot()

			for element in root.findall(recordDocQuery):
				text = cleansedRecords.reconstruct(element[0].text)
				dicts = getDicts(text)

				dumpMe = {
					"id": element.attrib["id"],
					"text": cleansedRecords.reconstruct(text),
					"type": recordFolder,
					"uni": dicts[0],
					"bi": dicts[1],
					"tri": dicts[2]
				}

				writeFile = open("%s/%s.json" % (outputFolder, dumpMe["id"]), "w")
				writeFile.write(json.dumps(dumpMe, sort_keys=True, indent=4))
				writeFile.close()
				
def addToDict(key, value, refDict):
	if refDict.has_key(key):
		if refDict[key].has_key(value):
			refDict[key][value] = refDict[key][value] + 1
		else:
			refDict[key][value] = 1
	else:
		refDict[key] = { value: 1 }

def convertToProb(refDict):
	for key in refDict:
		totalCount = 0
		for subKey in refDict[key]:
			totalCount = totalCount + refDict[key][subKey]

		tc = float(totalCount)
		for subKey in refDict[key]:
			refDict[key][subKey] = refDict[key][subKey] / tc

def getDicts(text):
	words = re.split("\\s+", text)

	uniDict = {}
	biDict = {}
	triDict = {}

	firstWord = words[0]
	secondWord = words[1]

	for i in range(2, len(words)):
		currentWord = words[i]

		previousWord = words[i-1]
		prevprevWord = words[i-2]

		# unigrams are pretty much on their own
		if uniDict.has_key(prevprevWord):
			uniDict[prevprevWord] = uniDict[prevprevWord] + 1
		else:
			uniDict[prevprevWord] = 1 

		addToDict(previousWord, prevprevWord, biDict)
		addToDict(currentWord, prevprevWord + "~" + previousWord, triDict)

	# handle unigrams one off
	totalCount = 0
	for key in uniDict:
		totalCount = totalCount + uniDict[key]

	tc = float(totalCount)
	for key in uniDict:
		uniDict[key] = uniDict[key] / tc

	convertToProb(biDict)
	convertToProb(triDict)

	return (uniDict, biDict, triDict)

if __name__ == '__main__':
        main()