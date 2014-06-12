import sys
import imp
import mysql.connector
import classify
import utils
import sqlStatements

def main():
	# mysql connection
	cnx = mysql.connector.connect(
							user='admin', 
							password='onetwotree',
							host='192.168.1.5',
							database='patientdischarge')

	trainSql = sqlStatements.sentimentTypeCount["train"]
	testSql = sqlStatements.sentimentTypeCount["test"]
	resultSql = sqlStatements.sentimentTypeCount["result"]

	classifier = classify.Classify()

	# create the models from our input
	print "getting data"
	train_model = utils.createArrayFromMySql(cnx, trainSql)
	test_model = utils.createArrayFromMySql(cnx, testSql)

	# train the classifier
	print "training classifier"
	classifier.train(train_model)

	# predict the test model
	print "predicting"
	results = classifier.predict(test_model)

	# upload results
	print "uploading results"
	utils.uploadResultsToSql(cnx, results, resultSql)

if __name__ == '__main__':
	main()