import gensim
import numpy as np

# Load Google's pre-trained Word2Vec model.
model_file = '/Users/amineboubezari/Downloads/GoogleNews-vectors-negative300.bin'
saved_file = '/Users/amineboubezari/Downloads/wv_model'

#model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)
#word_vectors = model.wv
#word_vectors.save(saved_file)
wv = gensim.models.KeyedVectors.load(saved_file)

print (wv.most_similar_cosmul(
	positive=['happy'], topn=3)
)

vec1 = wv.word_vec("dog", use_norm=True)
vec2 = wv.word_vec("man", use_norm=True)
print (vec1)
print (vec2)
print (vec1 + vec2)

print (wv.similar_by_vector((vec1), topn=20, restrict_vocab=None))