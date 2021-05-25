from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD
from nltk.stem import WordNetLemmatizer
import sqlite3 as sql
import numpy as np
import random
import pickle
import nltk
import json
import csv


lemmatizer = WordNetLemmatizer()
words = []
classes = []
docs = []
letters_to_ignore = ['?', '!', '.', ',']

data_file = open('cleaned_data/data_with_stopW.json').read()
intents = json.loads(data_file)

for intent in intents['intents']:
    for question in intent['question']:
        list_of_word = nltk.word_tokenize(question)
        words.extend(list_of_word)
        docs.append((list_of_word, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])


words = [lemmatizer.lemmatize(word) for word in words if word not in letters_to_ignore]
words = sorted(set(words))

pickle.dump(words, open('pickle/with_stopW/words.pkl', 'wb'))
pickle.dump(classes, open('pickle/with_stopW/classes.pkl', 'wb'))


training = []
empty_out = [0] * len(classes)


for doc in docs:
    BoW = []
    word_patterns = doc[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        BoW.append(1) if word in word_patterns else BoW.append(0)

    output_row = list(empty_out)
    output_row[classes.index(doc[1])] = 1
    training.append([BoW, output_row])


random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])  # tag
train_y = list(training[:, 1])  # question


model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))


sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=10000, batch_size=5, verbose=1)

model.save('chat_model/with_stopW/chat_model.h5', hist)
print('Done')