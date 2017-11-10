import numpy as np
import nltk

word_file = open('/Users/amineboubezari/Downloads/home/swn/www/admin/dump/' + 
	'SentiWordNet_3.0.0_20130122.txt')
word_dict = {}

# map nltk tags to the tags in the word dataset
pos_transform = {}
pos_transform.update({noun:"n" for noun in ["NN", "NNS", "NNP", "NNP", "POS"]})
pos_transform.update({verb:"v" for verb in ["VB", "VBD", "VBG", "VBN","VBP", "VBZ"]})
pos_transform.update({adverb:"r" for adverb in ["RB", "RBR", "RBS"]})
pos_transform.update({adjective:"a" for adjective in ["JJ", "JJR", "JJS"]})
pos_transform.update({other:"none" for other in ["CC", "CD", "DT", "EX", "FW", "IN", "LS", "MD", 
							"PDT","PRP", "PRP$", "RP", "TO", "UH", "WDT", "WP", "WP$", "WRB"]})


def remove_symbols(word):
	for i, c in enumerate(word):
		if c == '#':
			return word[:i]

def parse_file():
	for e, line in enumerate(word_file):
		if line[0] == '#':
			continue
	
		line_arr = line.split()
		words = [remove_symbols(word) for word in line_arr if ('#' in word)]

		for word in words:
			if word not in word_dict:
				word_dict[word] = []

			word_dict[word].append(
				{"POS": line_arr[0], "ID": int(line_arr[1]), 
				"p_score": float(line_arr[2]), "n_score": float(line_arr[3]), 
				"o_score": (1. - float(line_arr[2]) - float(line_arr[3]))}
			)

def summation(scored_words):
	score = 0.
	for score_dict in scored_words:
		score += score_dict["p_score"] - score_dict["n_score"]
	return score

def objective(scored_words):
	score = 0.
	for score_dict in scored_words:
		score += score_dict["o_score"]
	return score

def score_text(text, score_func):
	"""
	Score function is a one-argument function that takes a list of tuples of 
	form 
	"""
	tokens = nltk.word_tokenize(text)
	tagged = nltk.pos_tag(tokens)
	scored_words = []

	for word, tag in tagged:
		print (word)
		found = False
		for label in word_dict[word]:
			if label["POS"] == pos_transform[tag]:
				scored_words.append(
					{score_type: label[score_type] for score_type in ["p_score", "n_score", "o_score"]}
				)
				found = True
				break	
		if not found:
			print ("pos not found")
			scored_words.append({score_type: 0. for score_type in ["p_score", "n_score", "o_score"]})

	print (scored_words)
	print (score_func(scored_words))
	return score_func(scored_words)

def print_tags():
	pos = []
	for word, labels in word_dict.items():
		for label in labels:
			if label["POS"] not in pos:
				pos.append(label["POS"])
	
	print (pos)

def main():
	parse_file()	
	print_tags()
	score_text("hello hater", objective)

main()