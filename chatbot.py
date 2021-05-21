import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='')

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('cleaned_data/data_remove_stop.json').read())

words = pickle.load(open('pickle/words.pkl', 'rb'))
classes = pickle.load(open('pickle/classes.pkl', 'rb'))
model = load_model('chat_model/chatter_model.h5')


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
    ERROR_THRESHOLD = 0.8
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
                result = random.choice(i['answer'])
                break
    except IndexError:
        result = "I don't understand!"
    return result

print('GO! Bot is running')

@bot.command()
async def siri(ctx, *, inp):
    message = inp
    ints = predict_class(message)
    res = get_response(ints, intents)
    inp = res
    print(inp)
    await ctx.send(inp)


bot.run(TOKEN)

'''testar att pusha till dev'''





