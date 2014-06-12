import os

features = [
	"subjsimple",
	"subjcomplex"
]

sources = [
	"intuitive",
	"textual"
]

bashScriptTemplate = """
sudo rm -r data/mallet
sudo mkdir data/mallet
python source/mallet/main.py %s %s
"""

def main():
	for feature in features:
		for source in sources:
			print "executing %s %s " % (source, feature)
			os.system(bashScriptTemplate % (source, feature))

if __name__ == '__main__':
	main()