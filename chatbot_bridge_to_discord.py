import json
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import random
import pickle

import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command()
async def siri(ctx, *, inp):
    with open("data/json_test/data_test_new.json") as file:
        data = json.load(file)

    model = keras.models.load_model('chat_model.h5')

    with open('pickle/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    with open('pickle/label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    max_len = 20

    inp = inp
    inp.lower()
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                                      truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for i in data['intents']:
        if i['tag'] == tag:
            inp = random.choice(i['answer'])

    await ctx.send(inp)

bot.run(TOKEN)