import adjectivesAdverbsFeature
import adjectivesFeature
import adverbsFeature
import nounsFeature
import pronounsFeature
import verbsFeature

import allSubjectiveWordsFeature
import posFeature
import subjectiveComplexFeature
import subjectiveSimpleFeature
import subjectiveWordSimpleFeature
import subjectiveWordComplexFeature
import subjectiveDiseaseUniqueFeature
import highestProbabilityFeature

import chunkFeature

import wordCountFeature
import wordCount2Feature
import wordCount3Feature
import baseNamedEntityFeature
import config

wordcount = "wordcount"
subjsimple = "subjsimple"
subjcomplex = "subjcomplex"
subjwordsimple = "subjwordsimple"
subjwordcomplex = "subjwordcomplex"
highestprobword = "highestprobword"
uniqueword = "uniqueword"
allSubjectiveWords = "allSubjectiveWords"
wordCount2 = "wordCount2"
wordCount3 = "wordCount3"
baseNamedEntity = "baseNamedEntity"
chunk = "chunk"

pos = "pos"
adjectiveAdverbs = "adjectiveAdverbs"
adjective = "adjective"
adverb = "adverb"
noun = "noun"
pronoun = "pronoun"
verb = "verb"

featureDesc = {
	wordcount: "custom word count",
	
	subjsimple: "genia - polarity counts without X",
	subjcomplex: "genia - polarity|type counts without X",
	
	subjwordsimple: "polar word with word count",
	subjwordcomplex: "subjective word complex with word count",
	highestprobword: "highest probability words to that disease",
	uniqueword: "unique words to that disease",
	allSubjectiveWords: "all words marked with subjective annotations",
	
	pos: "genia - pos count without X",
	adjectiveAdverbs: "genia - adjectives and adverbs",
	adjective: "genia - adjectives",
	adverb: "genia - adverbs",
	noun: "genia - nouns",
	verb: "genia - verbs",
	pronoun: "genia - pronouns",

	chunk: "genia - chunk with word count",

	wordCount2: "words without X pos",
	wordCount3: "words without X -LBR-, , . | -RRB- pos",
	baseNamedEntity: "genia named entity with count"
}

def setupwordcount():
	return [ wordCountFeature ]

def setupsubjsimple():
	subjectiveSimpleFeature.cacheRepoHash(config.connection)
	wordCount3Feature.cacheRepoHash(config.connection)
	return [ subjectiveSimpleFeature, wordCount3Feature ]

def setupsubjcomplex():
	subjectiveComplexFeature.cacheRepoHash(config.connection)
	wordCount3Feature.cacheRepoHash(config.connection)
	return [ subjectiveComplexFeature, wordCount3Feature ]

def setupsubjwordsimple():
	subjectiveWordSimpleFeature.cacheRepoHash(config.connection)
	return [ subjectiveWordSimpleFeature, wordCountFeature ]

def setupsubjwordcomplex():
	subjectiveWordComplexFeature.cacheRepoHash(config.connection)
	return [ subjectiveWordComplexFeature, wordCountFeature ]

def setuphighestprobword():
	highestProbabilityFeature.cacheRepoHash(config.connection)
	return [ highestProbabilityFeature, wordCountFeature ]

def setupuniqueword():
	subjectiveDiseaseUniqueFeature.cacheRepoHash(config.connection)
	return [ subjectiveDiseaseUniqueFeature, wordCountFeature]

def setupallSubjectiveWordsFeature():
	allSubjectiveWordsFeature.cacheRepoHash(config.connection)
	return [ allSubjectiveWordsFeature, wordCountFeature ]

def setupPosFeature():
	posFeature.cacheRepoHash(config.connection, 2)
	wordCount3Feature.cacheRepoHash(config.connection)
	return [ posFeature, wordCount3Feature ]

def setupadjectiveAdverbsFeature():
	adjectivesAdverbsFeature.cacheRepoHash(config.connection, 2)
	return [ adjectivesAdverbsFeature, wordCountFeature ]

def setupadjectivesFeature():
	adjectivesFeature.cacheRepoHash(config.connection, 2)
	return [ adjectivesFeature, wordCountFeature ]

def setupadverbsFeature():
	adverbsFeature.cacheRepoHash(config.connection, 2)
	return [ adverbsFeature, wordCountFeature ]

def setupnounsFeature():
	nounsFeature.cacheRepoHash(config.connection, 2)
	return [ nounsFeature, wordCountFeature ]

def setuppronounsFeature():
	pronounsFeature.cacheRepoHash(config.connection, 2)
	return [ pronounsFeature, wordCountFeature ]

def setupverbsFeature():
	verbsFeature.cacheRepoHash(config.connection, 2)
	return [ verbsFeature, wordCountFeature ]

def setupwordCount2Feature():
	wordCount2Feature.cacheRepoHash(config.connection)
	return [ wordCount2Feature ]

def setupwordCount3Feature():
	wordCount3Feature.cacheRepoHash(config.connection)
	return [ wordCount3Feature ]

def setupbaseNamedEntityFeature():
	baseNamedEntityFeature.cacheRepoHash(config.connection)
	return [ baseNamedEntityFeature, wordCountFeature ]

def setupbaseChunkFeature():
	chunkFeature.cacheRepoHash(config.connection)
	return [ chunkFeature, wordCountFeature ]

features = { 
	wordcount: setupwordcount,
	subjsimple: setupsubjsimple,
	subjcomplex: setupsubjcomplex,
	subjwordsimple: setupsubjwordsimple,
	subjwordcomplex: setupsubjwordcomplex,
	uniqueword: setupuniqueword,
	highestprobword: setuphighestprobword,
	allSubjectiveWords: setupallSubjectiveWordsFeature,
	pos: setupPosFeature,
	adjectiveAdverbs: setupadjectiveAdverbsFeature,
	adjective: setupadjectivesFeature,
	adverb: setupadverbsFeature,
	noun: setupnounsFeature,
	pronoun: setuppronounsFeature,
	verb: setupverbsFeature,
	wordCount2: setupwordCount2Feature,
	wordCount3: setupwordCount3Feature,
	baseNamedEntity: setupbaseNamedEntityFeature,
	chunk: setupbaseChunkFeature
}