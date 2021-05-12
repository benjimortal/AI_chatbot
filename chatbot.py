import random
import json
import pickle
import numpy as np
import keyboard

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('data/json/data.json').read())

words = pickle.load(open('pickle/words.pkl', 'rb'))
classes = pickle.load(open('pickle/classes.pkl', 'rb'))
model = load_model('chatbot_save_model')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list



def get_response(ints, intents_json):
    try:
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = i['answer']
                break
    except IndexError:
        result = "I don't understand!"
    return result


def write_json(data, filename='data/json/user_train.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

with open('data/json/user_train.json') as json_file:
    data = json.load(json_file)
    temp = data

    print("werent you happy with your answer? press § to add one")
    restart = True
    while restart:
        message = input('')
        ints = predict_class(message)
        res = get_response(ints, intents)
        print(res)
        while True:
            if keyboard.read_key() == "§":

                answer = input(("enter what answer you want"))
                temp.append(
                    {
                        "tag": message,
                        "question": message,
                        "answer": answer
                    }
                )
                write_json(data)
                break













