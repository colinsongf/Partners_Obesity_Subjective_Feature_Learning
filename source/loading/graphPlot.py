import mysql.connector
import numpy as np
import matplotlib.pyplot as plt 

sql = """select 
	diseaseName,
	score,
	(select featureselectionname from classifierresults where macrof1score = score limit 1) as featureName
from (
select
	diseaseName,
	max(MacroF1Score) as score
from classifierresults
where source is null
group by diseasename
union
select
	diseaseName,
	MacroF1Score as score
from classifierresults
where source is null 
and FeatureSelectionName = 'mallet custom count baseline'
) b
order by DiseaseName asc, featureName asc
"""

featureNameHash = {
	"mallet custom count baseline":"bl",
	"subjectiveComplexFeature":"sc",
	"subjectiveDiseaseUniqueFeature":"sdu",
	"subjectiveSimpleFeature":"ss",
	"subjectiveWordComplexFeature":"swc",
	"highestProbFeature":"hp"
}

def get(connection):
	cursor = connection.cursor(buffered=True)

	X = []
	Y = []

	cursor.execute(sql)

	for row in cursor:
		diseaseName = row[0]
		score = float(row[1])
		featureName = row[2]

		X.append("%s %s" % (diseaseName, featureNameHash[featureName]))
		Y.append(score)

	fig = plt.figure()

	width = .99
	ind = np.arange(len(Y))
	plt.bar(ind, Y)
	plt.xticks(ind + width / 2, X)
	fig.autofmt_xdate()

	plt.savefig("results.pdf")