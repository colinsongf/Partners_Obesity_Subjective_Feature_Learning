import re

insertNoiseWordTemplate = ("insert into patientdischarge.noisewords(word) "
						"values (%s)")

whiteSpace = "\\s+"
singleSpace = " "

def insert(connection, fileLocation):
	cursor = connection.cursor(buffered=True)

	noiseWords = open(fileLocation, "r").read()
	words = re.split(whiteSpace, noiseWords)

	uniqueHash = {}
	for word in words:
		if not uniqueHash.has_key(word):
			uniqueHash[word] = None
			print word
			cursor.execute(insertNoiseWordTemplate, (word,))

	connection.commit()
	connection.close()

