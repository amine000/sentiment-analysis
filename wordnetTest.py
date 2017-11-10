from nltk.corpus import wordnet as wn

cookie = wn.synset('cookie.n.01')
angry = wn.synset('anger.n.01')
balloon = wn.synset('balloon.n.01')

# print("Balloon to angry: " + str(balloon.lch_similarity(angry)))
# print("Cookie to angry: " + str(cookie.lch_similarity(angry)))
# print("Balloon to cookie: " +str(balloon.lch_similarity(cookie)))
print("JESUS TO NIGGA : " + str(wn.synset("dick.n.02").wup_similarity(wn.synset("sex.n.01"))))
print(wn.synset("penis.n.01").definition())