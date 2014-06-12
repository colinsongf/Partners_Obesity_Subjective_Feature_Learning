from sklearn.ensemble import RandomForestClassifier
import numpy as np

class Classify:
	def __init__(self):
		self.forest = RandomForestClassifier(n_estimators=100)

	def train(self, train_data):

		X = train_data[0::, 1::]
		y = train_data[0::, 0]

		self.forest.fit(X, y)

	def predict(self, test_data):
		ids = test_data[0::, 0]
		actualData = test_data[0::, 1::]

		output = self.forest.predict(actualData)

		returnArray = [ ]

		for i in range(0, len(output)):
			returnArray.append((str(ids[i]), str(output[i])))

		return returnArray