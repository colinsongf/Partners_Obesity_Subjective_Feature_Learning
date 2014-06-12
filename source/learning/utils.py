import numpy as np
import csv as csv
import re
import os

def createArrayFromMySql(connection, selectSql):
	selectCursor = connection.cursor(buffered=True)
	selectCursor.execute(selectSql)

	list_data = []

	for row in selectCursor:
		list_data.append(row[0:])

	selectCursor.close()

	return np.array(list_data)

def uploadResultsToSql(connection, results, insertSql):
	insertCursor = connection.cursor(buffered=True)
	
	i = 0
	for result in results:
		print result
		insertCursor.execute(insertSql, result)

		if i % 100 == 0:
			connection.commit()

		i = i + 1

	connection.commit()

	insertCursor.close()

def createArrayFromCsvFile(csvFile):
	csv_file_object = csv.reader(open(csvFile, 'rb'))

	header = csv_file_object.next()

	list_data =[]

	for row in csv_file_object: 
	    list_data.append(row[0:]) 

	return np.array(list_data)

def createCsvFileFromArray(array, fileName):
	open_file_object = csv.writer(open(fileName, "wb"))

	for row in array:
		open_file_object.writerow(row)