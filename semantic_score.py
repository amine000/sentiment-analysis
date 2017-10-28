word_file = open('/Users/amineboubezari/Downloads/home/swn/www/admin/dump/SentiWordNet_3.0.0_20130122.txt')
word_dict = {}

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
				{"POS": line_arr[0], "ID": int(line_arr[1]), "p_score": float(line_arr[2]),
				  "n_score": float(line_arr[3]), "o_score": (1. - float(line_arr[2]) - float(line_arr[3]))}
			)

def main():
	parse_file()
	print (word_dict['hate'])

main()