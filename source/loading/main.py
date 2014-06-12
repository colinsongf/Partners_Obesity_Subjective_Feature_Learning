import mysql.connector
import xml.etree.ElementTree as ET
from os import listdir
import record
import clusters
import pos
import sections
import subjectiveLexicon
import cleansedRecords
import noiseWords
import diseaseUniqueWords
import diseaseHighestProb
import genia

# expecting to be executed from root folder
obesityTrainingFolder = "data/train"
obesityTestFolder = "data/test"
obesityAnnotationFolder = "data/annotations"

jsonFolder = "data/json"
posFolder = "data/pos"
sectionsInputFolder = "data/stanfordPos/Input"
sectionsOutputFolder = "data/stanfordPos/Output"

jarFile = "data/stanfordPos/CohortFinderNLP.jar"
keyFile = "keyFile.txt"
subjectiveLexiconFile = "data/subjectiveLexicon/lexicon.txt"
noiseWordsFile = "data/noiseWords.txt"

geniaInput = "../data/genia/Input"
geniaIntermediate = "../data/genia/Intermediate"
geniaOutput = "../data/genia/Output"

def main():
	cnx = mysql.connector.connect(
								user='admin', 
								password='onetwotree',
								host='192.168.1.5',
								database='patientdischarge')

	# record.insertRecords([obesityTrainingFolder, obesityTestFolder], cnx)
	# record.insertAnnotations(obesityAnnotationFolder, cnx)
	# record.insertNgrams(jsonFolder, cnx)
	# cleansedRecords.insertRecords([obesityTrainingFolder, obesityTestFolder], cnx)
	# cleansedRecords.insertNgrams(jsonFolder, cnx)

	# clusters.insertClusters(cnx)
	# pos.insertPos(cnx, posFolder)
	# sections.saveSections([obesityTrainingFolder, obesityTestFolder], sectionsInputFolder)
	# sections.sectionPosConvert(jarFile, keyFile, sectionsInputFolder, sectionsOutputFolder)
	# sections.insertSections(cnx, sectionsInputFolder)
	# sections.insertSentences(cnx, sectionsOutputFolder)
	# subjectiveLexicon.insertRecords(cnx, subjectiveLexiconFile)

	# noiseWords.insert(cnx, noiseWordsFile)

	# diseaseUniqueWords.calculateUniqueWords(cnx)
	# diseaseHighestProb.calculateUniqueWords(cnx)

	# graphPlot.get(cnx)

	# genia.outputGeniaTag(geniaInput, geniaIntermediate, geniaOutput)
	genia.insertGeniaTag(geniaOutput, cnx)

if __name__ == '__main__':
        main()