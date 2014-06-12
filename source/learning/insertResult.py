import mysql.connector

insertResultTemplate = """
insert into patientdischarge.ClassifierResults(FeatureSelectionName, ClassifierName, Count, DiseaseName, MicroF1Score, MacroRecall, MacroPrecision, MacroF1Score) 
values (%s, %s, %s, %s, %s, %s, %s, %s)
"""

insertAggregateResultTemplate = """
insert into patientdischarge.ClassifierAggregateResults(MicroF1Score, MacroRecall, MacroPrecision, MacroF1Score, Type) 
values (%s, %s, %s, %s, %s)
"""

def insertClassifierResults(connection, resultTuple):
	cursor = connection.cursor(buffered=True)
	cursor.execute(insertResultTemplate, resultTuple)
	connection.commit()
	print "submitted " + str(resultTuple)

def insertAggregateResults(connection, resultTuple):
	cursor = connection.cursor(buffered=True)
	cursor.execute(insertAggregateResultTemplate, resultTuple)
	connection.commit()
	print "submitted " + str(resultTuple)