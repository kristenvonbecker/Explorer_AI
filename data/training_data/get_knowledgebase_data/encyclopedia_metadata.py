import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()


# define parameters for API calls to the Encyclopedia Britannica products

url_base = {
    'advanced': 'https://syndication.api.eb.com/production/articles?articleTypeId=1&page=',
    'concise': 'https://syndication.api.eb.com/production/articles?articleTypeId=45&page=',
    'intermediate': 'https://syndication.api.eb.com/production/articles?articleTypeId=31&page='
}

headers = {
    'advanced': {
        'x-api-key': os.getenv('EB_API_KEY_ADV'),
        'content-type': 'application/json'
    },
    'concise': {
        'x-api-key': os.getenv('EB_API_KEY_CON'),
        'content-type': 'application/json'
    },
    'intermediate': {
        'x-api-key': os.getenv('EB_API_KEY_INT'),
        'content-type': 'application/json'
    }
}

# get metadata for all entries (articles) in each source
# save to dir_path with filename <source>.json


def get_encyclopedia_metadata(source, dir_path):
    article_metadata = []

    code = 200
    page = 1

    url = url_base[source] + str(page)
    response = requests.get(url, headers=headers[source])

    while code == 200 and page < 100:
        this_data = json.loads(response.text)['articles']
        article_metadata += this_data
        page += 1
        url = url_base[source] + str(page)
        response = requests.get(url, headers=headers[source])
        code = response.status_code

    path = dir_path
    if not os.path.exists(path):
        os.makedirs(path)

    filepath = os.path.join(path, source + '.json')
    if os.path.exists(filepath):
        os.remove(filepath)

    with open(filepath, 'w') as outfile:
        json.dump(article_metadata, outfile, indent=2)

    return article_metadata
