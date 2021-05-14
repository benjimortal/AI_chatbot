import json
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder





import random
import pickle

with open("data/json/data.json") as file:
    data = json.load(file)



# load trained model
model = keras.models.load_model('chat_model.h5')

# load tokenizer object
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load label encoder object
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# parameters
max_len = 20
print('Bot is running')
while True:

    inp = input()
    if inp.lower() == "quit":
        break

    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                                      truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for i in data['intents']:
        if i['tag'] == tag:
            print(i['answer'])

    # print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,random.choice(responses))