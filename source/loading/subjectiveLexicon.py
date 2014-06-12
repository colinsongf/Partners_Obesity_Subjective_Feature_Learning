import re
import mysql.connector

whiteSpace = "\s+"

equalSign = "="

insertCommand = ("insert into patientdischarge.subjectivelexicon(Type, Len, Word, Pos, Stemmed, PriorPolarity)"
				"values (%s, %s, %s, %s, %s, %s)")

def insertRecords(connection, lexiconFile):
	cursor = connection.cursor(buffered=True)
	# read in the example sentences
	lexiconFileStream = open(lexiconFile)
	line = lexiconFileStream.readline().strip()

	count = 0
	while line:
		count = count + 1
		items = re.split(whiteSpace, line)

		cleansedValues = []
		for item in items:
			values = item.split(equalSign)
			cleansedValues.append(values[1])

		# time to insert
		tup = (cleansedValues[0], cleansedValues[1], cleansedValues[2], cleansedValues[3], cleansedValues[4], cleansedValues[5])
		print tup
		cursor.execute(insertCommand, tup)

		if count % 100 == 0:
			connection.commit()

		line = lexiconFileStream.readline().strip()

	connection.commit()