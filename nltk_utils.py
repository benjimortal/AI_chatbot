import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
nltk.download('punkt')


def token(sentence):
    return nltk.word_tokenize(sentence)


def stemming(word):
    return stemmer.stem(word.lower())


def bow(tokenized_sentence, words):
    word_sentence = [stemming(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.int8)
    for id, w in enumerate(words):
        if w in word_sentence:
            bag[id] = 1
    return bag
