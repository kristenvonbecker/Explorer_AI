import requests
from lxml import html
import os
import json
import xmltodict
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
load_dotenv()

# define parameters for API calls to the Encyclopedia Britannica products

header = {
    'advanced': {
        'x-api-key': os.getenv('EB_API_KEY_ADV'),
        'content-type': 'text/xml; charset=UTF-8'
    },
    'intermediate': {
        'x-api-key': os.getenv('EB_API_KEY_INT'),
        'content-type': 'text/xml; charset=UTF-8'
    },
    'concise': {
        'x-api-key': os.getenv('EB_API_KEY_CON'),
        'content-type': 'text/xml; charset=UTF-8'
    }
}

source_code = {
    'advanced': 1,
    'intermediate': 31,
    'concise': 45,
}


def get_pre_header_text(article_id, source, dir_path=None):
    url = f'https://syndication.api.eb.com/production/article/{str(article_id)}/xml'
    response = requests.get(url, headers=header[source])
    tree = html.fromstring(response.content)
    title = tree.xpath("//article")[0].xpath("title/text()")[0]
    article_id = int(tree.xpath("//article")[0].xpath("@articleid")[0])
    data = {
        'title': title,
        'article_id': article_id,
        'source_code': source_code[source],
        'text': '',
    }
    article = tree.xpath("//article/*")
    h1 = False
    for elmt in article:
        if elmt.tag == 'h1':
            h1 = True
        elif elmt.tag == 'p' and not h1:
            data['text'] += ''.join(elmt.xpath("text()|xref/text()|e/text()|xref/e/text()"))
    if dir_path:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        filepath = os.path.join(dir_path, str(article_id) + '.json')
        if os.path.exists(filepath):
            os.remove(filepath)
        with open(filepath, 'w') as outfile:
            outfile.write(json.dumps(data, indent=2))
    return data
