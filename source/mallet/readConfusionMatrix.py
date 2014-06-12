import re

labelRegex = re.compile("label")

whiteSpace = "\\s+"

def readText(stdOutText):
	lines = stdOutText.split("\n")

	foundConfusion = False
	
	confusionMatrix = []
	confusionLabelDict = {}

	for line in lines:
		if labelRegex.match(line):
			foundConfusion = True
			continue

		if foundConfusion == True:
			if len(line.strip()) == 0:
				break

			items = re.split(whiteSpace, line.strip())

			newRow = []

			matrixLabel = 0
			for i in range(0, len(items) - 1):
				if i == 0:
					matrixLabel = items[i]
					continue
				if i == 1:
					confusionLabelDict[matrixLabel] = items[i]
					continue

				item = convertInt(items[i])
				newRow.append(item)

			confusionMatrix.append(newRow)
	
	y_truth = []
	y_pred = []
	trueCount = 0

	for truth in range(0, len(confusionMatrix)):
		subArray = confusionMatrix[truth]
		for pred in range(0, len(subArray)):
			totalCount = subArray[pred]

			if truth == pred:
				y_truth.append(truth)
				y_pred.append(pred)
				trueCount = trueCount + totalCount

			for i in range(0, totalCount):
				y_truth.append(truth)
				y_pred.append(pred)

	return (confusionMatrix, confusionLabelDict, y_truth, y_pred, trueCount)

def convertInt(value):
	try:
		i = int(value)
		return i
	except ValueError:
		return 0