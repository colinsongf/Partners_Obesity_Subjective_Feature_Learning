import re

selectWordWeightGroup = """
select 
	word,
	avgprob,
	type
from patientdischarge.wordweightgroup
"""

insertDiseaseUniqueWords = """
insert into patientdischarge.diseaseuniquewords(word, disease) 
values (%s, %s)
"""

whiteSpace = "\\s+"
singleSpace = " "

def calculateUniqueWords(connection):
	cursor = connection.cursor(buffered=True)

	cursor.execute(selectWordWeightGroup)
	
	internalRepo = {}

	for wordWeight in cursor:
		word = wordWeight[0]
		count = float(wordWeight[1])
		disease = wordWeight[2]

		if not internalRepo.has_key(disease):
			internalRepo[disease] = { word: None }
		else: 
			internalRepo[disease][word] = None

	cursor.close()
	uniqueWordRepo = {}

	for diseaseKey in internalRepo:
		# set up to begin with
		uniqueWordRepo[diseaseKey] = {}

		for word in internalRepo[diseaseKey]:

			# let's make sure this word doesn't exist in any other dictionary
			exists = False
			for otherDiseaseKey in internalRepo:
				if otherDiseaseKey == diseaseKey:
					continue

				if internalRepo[otherDiseaseKey].has_key(word):
					exists = True
					break

			if not exists:
				uniqueWordRepo[diseaseKey][word] = None

	cursor = connection.cursor(buffered=True)
	# now, go through other repo and upload results
	for diseaseKey in uniqueWordRepo:
		for wordKey in uniqueWordRepo[diseaseKey]:
			cursor.execute(insertDiseaseUniqueWords, (wordKey, diseaseKey))

	connection.commit()
	cursor.close()