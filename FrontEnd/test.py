# from nltk.tag import StanfordPOSTagger

# st = StanfordPOSTagger("models\english-bidirectional-distsim.tagger", "\\")

# jigga = input("What's up: ")
# print(st.tag(jigga.split()))
import nltk.parse.stanford as fuck
import nltk
from nltk.corpus import brown
import os

os.environ['CLASSPATH']='C:\\Users\\Kyung-Min\\Documents\\CS\\CS101\\stanford-parser-full-2017-06-09'
os.environ['STANFORD-MODELS']='C:\\Users\\Kyung-Min\\Documents\\CS\\CS101\\stanford-parser-full-2017-06-09'
os.environ['JAVAHOME']='C:\\ProgramData\\Oracle\\Java\\javapath'
parser = fuck.StanfordParser(model_path="C:\\Users\\Kyung-Min\\Documents\\CS\\CS101\\stanford-parser-full-2017-06-09\\edu\\stanford\\nlp\\models\\lexparser\\englishPCFG.ser.gz")

def rarity(word, fdist):
	rarity = 0
	if (word in fdist):
		rarity = fdist[word]
	return rarity

def rare_word(message, fdist):
	rarest_score = 99999
	best = ''
	fufu = nltk.word_tokenize(message)
	for word in fufu:
		# Rarity of most common association of word
		score = rarity(word, fdist)
		if score < rarest_score:
			best = word
			rarest_score = score
	#print (word, rarest_score)
	return best

def keywords(message, fdist):
	potential_keywords = []
	fufu = nltk.word_tokenize(message)
	#print(fufu)
	shiieeeetttttt = parser.parse(fufu)
	for x in shiieeeetttttt:
		#x.pretty_print()

		# First, look for direct object
		# S -> VP -> NP -> NN
		for vp in x.subtrees(lambda t: t.label() == "VP"):
				for np in vp.subtrees(lambda t: t.label() == "NP"):
					for do in np.subtrees(lambda t: t.label().count("JJ") > 0):
						if (do.leaves()[0] not in potential_keywords):
							potential_keywords.append(do.leaves()[0])	
					for do in np.subtrees(lambda t: t.label().count("NN") > 0):
						if (do.leaves()[0] not in potential_keywords):
							potential_keywords.append(do.leaves()[0])	
		if (len(potential_keywords) <= 1):
			# Try object of prepositional phrase
			for pp in x.subtrees(lambda t: t.label() == "PP"):
					for noun in pp.subtrees(lambda t: t.label().count("NN") > 0):
						if (noun.leaves()[0] not in potential_keywords):
							potential_keywords.append(noun.leaves()[0])	

		# ADJ PHRASES ARE THE BEST
		if (len(potential_keywords) <= 1):
			for adjp in x.subtrees(lambda t: t.label() == "ADJP"):
				for adj in adjp.subtrees(lambda t: t.label() == "JJ"):
						if (adj.leaves()[0] not in potential_keywords):
							potential_keywords.append(adj.leaves()[0])	
		if (len(potential_keywords) <= 3):
			# Get verbs
			for verb in x.subtrees(lambda t: t.label().count("VB") > 0):
				first = verb.leaves()[0]
				if (first not in potential_keywords):
					if (rarity(first, fdist) <= 3):
						potential_keywords.append(verb.leaves()[0])	
		if (len(potential_keywords) == 0):
			# Otherwise just get any noun
			for noun in x.subtrees(lambda t: t.label().count("NN") > 0):
				if (noun.leaves()[0] not in potential_keywords):
					potential_keywords.append(noun.leaves()[0])	
	if (len(potential_keywords) == 0):
		potential_keywords.append(fufu[0])

	rarest_word = rare_word(message, fdist)
	#print (rarest_word)
	if (rarest_word not in potential_keywords):
		potential_keywords.append(rarest_word)
	return potential_keywords

# text = brown.words(categories=['news', 'editorial','humor','reviews','fiction','lore'])
# fdist = nltk.FreqDist(w.lower() for w in text)
# while (True):
# 	s = input()
# 	print(rarity(s,fdist))