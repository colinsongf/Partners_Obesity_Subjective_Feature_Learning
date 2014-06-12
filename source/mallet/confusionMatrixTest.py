import readConfusionMatrix
import numpy as np
from sklearn import metrics
from sklearn.metrics import precision_recall_fscore_support

def main():
	f = open("me.stdout", "r").read()

	print f
	
	(confusionMatrix, labels, ytrue, ypred, trueCount) = readConfusionMatrix.readText(f)
	for row in confusionMatrix:
		print row

	precisionMicro = np.float(metrics.precision_score(ytrue, ypred, average="micro"))
	recallMicro = np.float(metrics.recall_score(ytrue, ypred, average="micro"))
	f1Micro = np.float(metrics.f1_score(ytrue, ypred, average="micro"))
	f1Macro = np.float(metrics.f1_score(ytrue, ypred, pos_label=1, average="macro"))
	precisionMacro = np.float(metrics.precision_score(ytrue, ypred, average="macro"))
	recallMacro = np.float(metrics.recall_score(ytrue, ypred, average="macro"))

	mConf = metrics.confusion_matrix(ytrue, ypred)
	print mConf

	print labels
	print len(ytrue)
	print len(ypred)
	print trueCount

	print metrics.accuracy_score(ytrue, ypred)

	print precisionMicro
	print recallMicro
	print f1Micro
	print f1Macro
	print precisionMacro
	print recallMacro

if __name__ == '__main__':
	main()