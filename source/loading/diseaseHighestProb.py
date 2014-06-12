import re

selectWordWeightGroup = """
select 
	word,
	avgprob,
	type
from patientdischarge.wordweightgroup
"""

insertDiseaseUniqueWords = """
insert into patientdischarge.diseasehighestprobwords(word, disease, avgprob) 
values (%s, %s, %s)
"""

whiteSpace = "\\s+"
singleSpace = " "

avgProbKey = "avgProb"

def calculateUniqueWords(connection):
	cursor = connection.cursor(buffered=True)

	cursor.execute(selectWordWeightGroup)
	
	internalRepo = {}

	for wordWeight in cursor:
		word = wordWeight[0]
		avgProb = float(wordWeight[1])
		disease = wordWeight[2]

		if not internalRepo.has_key(disease):
			internalRepo[disease] = { word: { avgProbKey: avgProb } }
		else: 
			internalRepo[disease][word] = { avgProbKey: avgProb }

	cursor.close()
	uniqueWordRepo = {}

	for diseaseKey in internalRepo:
		# set up to begin with
		uniqueWordRepo[diseaseKey] = { }

		for word in internalRepo[diseaseKey]:

			# let's make sure this word doesn't exist in any other dictionary
			wordSumProb = internalRepo[diseaseKey][word][avgProbKey]
			isHighestSumProb = True
			
			for otherDiseaseKey in internalRepo:
				if otherDiseaseKey == diseaseKey:
					continue

				if (internalRepo[otherDiseaseKey].has_key(word) and 
					internalRepo[otherDiseaseKey][word][avgProbKey] > wordSumProb):
					isHighestSumProb = False
					break

			print "processing " + diseaseKey + " " + word
			if isHighestSumProb:
				uniqueWordRepo[diseaseKey][word] = wordSumProb

	cursor = connection.cursor(buffered=True)
	# now, go through other repo and upload results
	idx = 0
	for diseaseKey in uniqueWordRepo:
		for wordKey in uniqueWordRepo[diseaseKey]:
			idx = idx + 1
			cursor.execute(insertDiseaseUniqueWords, (wordKey, diseaseKey, uniqueWordRepo[diseaseKey][wordKey]))
			
			if idx > 5000:
				print 'committing ' + str(len(uniqueWordRepo[diseaseKey]))
				connection.commit()
				idx = 0


		print 'committing ' + str(len(uniqueWordRepo[diseaseKey]))
		connection.commit()
		idx = 0
	
	cursor.close()