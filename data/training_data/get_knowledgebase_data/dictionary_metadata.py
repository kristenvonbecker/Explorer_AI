import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

# define parameters for API calls to the Merriam-Webster products

url_base = {
    'dictionary': 'https://www.dictionaryapi.com/api/v3/references/collegiate/json',
    'thesaurus': 'https://www.dictionaryapi.com/api/v3/references/thesaurus/json'
}

headers = {
    'dictionary': {
        'x-api-key': os.getenv('MW_API_KEY_DICT'),
        'content-type': 'application/json'
    },
    'thesaurus': {
        'x-api-key': os.getenv('MW_API_KEY_THES'),
        'content-type': 'application/json'
    }
}

# get entry in the specified source which corresponds to the given entity
# e.g. get_metadata('afterimage', 'dictionary')


# the code below is NOT functional

def get_metadata(entity, source):
    url = url_base[source] + entity
    response = requests.get(url, headers=headers[source])

    this_data = json.loads(response.text)

    return this_data

