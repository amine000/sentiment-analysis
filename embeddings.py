import gensim

# Load Google's pre-trained Word2Vec model.
model_file = '/Users/amineboubezari/Downloads/GoogleNews-vectors-negative300.bin'
saved_file = '/Users/amineboubezari/Downloads/wv_model'

#model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)
#word_vectors = model.wv
#word_vectors.save(saved_file)
wv = gensim.models.KeyedVectors.load(saved_file)

print (wv.most_similar(
	positive=['angry'], negative=['calm'], topn=30)
)