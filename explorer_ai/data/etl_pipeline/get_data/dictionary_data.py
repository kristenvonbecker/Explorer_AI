import requests
from fuzzywuzzy import fuzz
from spellchecker import SpellChecker
import os
import json
from dotenv import load_dotenv

load_dotenv()
spell = SpellChecker()


api_key = os.getenv('MW_API_KEY_DICT')


def spell_check(phrase):
    words = phrase.split()
    fixed = [spell.correction(word) or word for word in words]
    fixed_phrase = ' '.join(fixed) if fixed else phrase
    return fixed_phrase


def get_url(search_term, api_key):
    search_term = '-'.join(search_term.split())
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{search_term}?key={api_key}'
    return url


def get_dict_entry(text):
    url = get_url(text, api_key)
    response = requests.get(url).json()
    if response:
        if isinstance(response[0], dict):
            return response


def get_dict_data(search_terms, dir_path=None):
    dict_data = []
    for term in search_terms:
        response = get_dict_entry(term)
        if response:
            dict_data.append(response)
            if dir_path:
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
                term = '-'.join(term.split())
                filepath = os.path.join(dir_path, term + '.json')
                if os.path.exists(filepath):
                    os.remove(filepath)
                with open(filepath, 'w') as outfile:
                    outfile.write(json.dumps(response, indent=2))

    return dict_data
