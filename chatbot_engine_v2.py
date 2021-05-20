import nltk
import json
import pickle
import numpy as np
import random

from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
lemmatizer = WordNetLemmatizer()

words = []
classes = []
docs = []
letters_to_ignore = ['?', '!', '.', ',']

training = []
BoW = []

data_file = open('data/json/data.json').read()
intents = json.loads(data_file)


def dataset_to_lists(intents, docs, words, classes):

    for intent in intents['intents']:
        for question in intent['question']:
            list_of_word = nltk.word_tokenize(question)
            words.extend(list_of_word)
            docs.append((list_of_word, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    return words, classes, docs


def lemmatize(words, letters_to_ignore):
    words = [lemmatizer.lemmatize(word) for word in words if word not in letters_to_ignore]
    return words


def sort_words(words):
    words = sorted(set(words))
    return words


def pickle_words_and_classes(words, classes):
    pickle.dump(words, open('pickle/words.pkl', 'wb'))
    pickle.dump(classes, open('pickle/classes.pkl', 'wb'))
    return words, classes


def prepare_training(docs, words, empty_out):

    empty_out = [0] * len(classes)

    for doc in docs:
        word_patterns = doc[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            if word in word_patterns:
                BoW.append(1)
            else:
                BoW.append(0)

    return


def training_set(doc):
    training = []
    empty_out = [0] * len(classes)
    output_row = list(empty_out)
    output_row[classes.index(doc[1])] = 1
    training.append([BoW, output_row])


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
    print('Done')
    return model, hist


def start_chatbot_engine():
    print('Start engine')
    dataset_to_lists(intents, docs, words, classes)
    print('1. step : Done')
    lemmatize(words, letters_to_ignore)
    print('2. step : Done')
    sort_words(words)
    print('3. step : Done')
    pickle_words_and_classes(words, classes)
    print('4. step : Done')
    prepare_training(docs, words, classes, training)
    print('5. step : Done')
    neuron_train(training)


print(start_chatbot_engine())
print('Done')
