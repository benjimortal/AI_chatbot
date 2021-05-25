from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD
from nltk.stem import WordNetLemmatizer
import numpy as np
import random
import pickle
import nltk
import json


lemmatizer = WordNetLemmatizer()
words = []
classes = []
docs = []
letters_to_ignore = ['?', '!', '.', ',']

data_file = open('cleaned_data/data_removed_stopW.json').read()
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

pickle.dump(words, open('pickle/without_stopW/words.pkl', 'wb'))
pickle.dump(classes, open('pickle/without_stopW/classes.pkl', 'wb'))

training = []
empty_out = [0] * len(classes)

for doc in docs:
    BoW = []
    word_patterns = doc[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        BoW.append(1) if word in word_patterns else BoW.append(0)

    row_output = list(empty_out)
    row_output[classes.index(doc[1])] = 1
    training.append([BoW, row_output])

random.shuffle(training)
training = np.array(training)

x_train = list(training[:, 0])  # tag
y_train = list(training[:, 1])  # question

model = Sequential()
model.add(Dense(200, input_shape=(len(x_train[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(100, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)  #optimzer you can use if you want
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

run = model.fit(np.array(x_train), np.array(y_train), epochs=500, batch_size=5, verbose=1)

model.save('chat_model/without_stopW/chat_model.h5', run)
print('Done')