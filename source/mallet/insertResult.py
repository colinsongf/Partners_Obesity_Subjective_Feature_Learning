import mysql.connector

insertResultTemplate = """
insert into patientdischarge.ClassifierResults(FeatureSelectionName, ClassifierName, Count, DiseaseName, MicroPrecision, MicroRecall, MicroF1Score, MacroRecall, MacroPrecision, MacroF1Score, Source, Accuracy) 
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

insertAggregateResultTemplate = """
insert into patientdischarge.ClassifierAggregateResults(MicroPrecision, MicroRecall, MicroF1Score, MacroRecall, MacroPrecision, MacroF1Score, FeatureSet, Source, Accuracy) 
values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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