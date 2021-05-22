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
import math

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='')

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('cleaned_data/william_add_sometext.json').read())

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
    ERROR_THRESHOLD = 0.6
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

def mathadd(x:float, y: float):
    return x + y

def mathsub(x: float, y:float):
    return x - y

def mathmulti(x: float, y: float):
    return x * y

def mathsqrt(x:float):
    return math.sqrt(x)

def mathdiv(x: float, y: float):
    return x / y

def mathexp(x: float, y: float):
    return x ** y


@bot.command()
async def siri(ctx, *, inp):
    message = inp
    ints = predict_class(message)
    res = get_response(ints, intents)
    inp = res
    print(inp)
    await ctx.send(inp)


@bot.command()
async def add(ctx, x: float, y: float):
    result = mathadd(x, y)
    await ctx.send(result)

@bot.command()
async def sub(ctx, x: float, y: float):
    result = mathsub(x, y)
    await ctx.send(result)

@bot.command()
async def multi(ctx, x: float, y: float):
    result = mathmulti(x, y)
    await ctx.send(result)
@bot.command()
async def sqrt(ctx, x: float):
    result = mathsqrt(x)
    await ctx.send(result)

@bot.command()
async def div(ctx, x: float, y: float):
    result = mathdiv(x, y)
    await ctx.send(result)

@bot.command()
async def exp(ctx, x: float, y: float):
    result = mathexp(x, y)
    await ctx.send(result)

bot.run(TOKEN)