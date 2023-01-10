import json
import numpy as np
from tensorflow import keras
from keras.preprocessing.sequence import pad_sequences
import colorama
from colorama import Fore, Style
import pickle

colorama.init()

with open("intents.json", 'r') as infile:
    data = json.load(infile)


def chat():
    model = keras.models.load_model('chat_model')

    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    with open('label_encoder.pickle', 'rb') as enc:
        encoder = pickle.load(enc)

    max_len = 20

    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = input()
        if inp.lower() == "quit":
            break

        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=max_len))
        tag = encoder.inverse_transform([np.argmax(result)])

        for i in data['intents']:
            if i['intent'] == tag:
                print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL, i['response'])


print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)

chat()