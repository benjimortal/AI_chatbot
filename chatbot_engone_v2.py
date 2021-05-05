import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random


words = []
classes = []
docs = []
letters_to_ignore = ['?', '!', '.', ',']

intents_list = []
training = []
empty_out = [0] * len(classes)

data_file = open('data/json_test/data_test_new.json').read()
intents = json.loads(data_file)

first = [intents_list.append(intent) for intent in intents['intents']]


def dataset_to_list(intents_list):

    for line in intents_list:
        question = str(line['question'])
        question = question.replace('[','').replace(']','').replace("'","")
        list_of_word = nltk.word_tokenize(question)
        words.extend(list_of_word)
        tag = line['tag']
        docs.append((list_of_word, tag))
        if tag not in classes:
            classes.append(tag)
    return



def lemmatiz(words):
    words = [lemmatizer.lemmatize(word) for word in words if word not in letters_to_ignore]
    return words

def sort_words(words):
    words = sorted(set(words))
    return words


def pickle_words_and_classes(words, classes):
    pickle.dump(words, open('pickle/words_second.pkl', 'wb'))
    pickle.dump(classes, open('pickle/classes_second.pkl', 'wb'))
    return words, classes


def prepare_train(docs, words):
    for doc in docs:
        BoW = []
        word_patterns = doc[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            BoW.append(1) if word in word_patterns else BoW.append(0)

        output_row = list(empty_out)
        output_row[classes.index(doc[1])] = 1
        training.append([BoW, output_row])
    return


def neuron_train(training):
    random.shuffle(training)
    training = np.array(training)

    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

    model.save('chatbot_save_model', hist)

def start_chabot_engine():
    print('Start engine')
    dataset_to_list(intents_list)
    print('1. step: Done')
    lemmatiz(words)
    print('2. step: Done')
    sort_words(words)
    print('3. step: Done')
    pickle_words_and_classes(words, classes)
    print('4. step: Done')
    prepare_train(docs, words)
    print('5. step: Done')
    neuron_train(training)
    print('6. step: Done')

