import re

wordRegex = "[A-Za-z]+"

def get(data):
	words = {}

	text = data[1]
	for wordMatch in re.finditer(wordRegex, text):
		word = text[wordMatch.start():wordMatch.end()]

		if words.has_key(word):
			words[word] = words[word] + 1
		else:
			words[word] = 1

	wordCounts = []

	for key in words:
		wordCounts.append("%s %s" % (key, words[key]))

	return " ".join(wordCounts)
