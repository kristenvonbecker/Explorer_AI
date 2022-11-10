import os
from fuzzywuzzy import fuzz
import requests
from bs4 import BeautifulSoup
from lxml import etree
from spellchecker import SpellChecker

import json

spell = SpellChecker()


# load article lists
def load_article_list(path, filename):
    filepath = os.path.join(path, filename)
    with open(filepath, 'r') as file:
        data = json.load(file)
    for item in data:
        if item['title'] == '':
            data.remove(item)
    return data


# load list of search_terms
def load_search_terms(path, filename):
    filepath = os.path.join(path, filename)
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


# define spell-checker

def spell_check(phrase):
    words = phrase.split()
    fixed = [spell.correction(word) or word for word in words]
    fixed_phrase = ' '.join(fixed) if fixed else phrase
    return fixed_phrase


# get article titles which fall under a given topic (search_text)

def get_britannica_topic_titles(search_text):
    search_text = '-'.join(search_text.split())
    url = f'https://www.britannica.com/topic/{search_text}'
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    content = etree.HTML(str(soup))
    titles = content.xpath('//section[@class="index-entries"]//span[@class="index-xref"]/a/text()')
    titles = [title.split(': ')[0] for title in titles]
    unique_titles = []
    [unique_titles.append(x) for x in titles if x not in unique_titles]
    return unique_titles


# get the articleId of any article with a title that fuzzy matches with the search term
# default threshold = 1 (words are the same)
# source = articles_adv, articles_con, or articles_int

def get_articles_by_title(search_text, source, threshold=100):
    matches = [article for article in source if fuzz.ratio(article['title'], search_text) >= threshold]
    return matches


# get article metadata (from source) for a given search_term
# returns a list of dicts

def get_articles(search_text, source, threshold, adv_flag=False):
    # first try to match search_term against artitle titles
    # returns list of article metadata dicts
    matches = get_articles_by_title(search_text, source, threshold)

    # if that doesn't work and we're searching the advanced articles...
    if not matches and adv_flag:

        # try to match search_term against britannica "topic" names
        # get titles of articles under that topic
        titles = get_britannica_topic_titles(search_text)

        # if that doesn't work, try again, but first run search_text through a spell-checker
        if not titles:
            titles = get_britannica_topic_titles(spell_check(search_text))

        # for each title returned above, get the article metadata
        for title in titles:
            matches += get_articles_by_title(title, source)

    # return list of matches
    return matches


# get all EB matches for all search terms

def get_all_articles(search_terms, sources, threshold, path_out=None):
    # initialize matches
    article_matches = []

    for item in search_terms:
        # initialize matches for this item
        matches = []
        these_matches = {
            'search_term': item['primary'],
            'primary_articles': [],
            'related_articles': [],
        }

        # process the primary search term through each of the sources
        search_text = item['primary']
        for i, source in enumerate(sources):
            flag = i == 0
            matches += get_articles(search_text, source, threshold, adv_flag=flag)

        # append any matches to the 'primary_articles' key
        these_matches['primary_articles'] += matches

        # if no matches were found for the primary search term
        # process any related search terms
        if not matches and item['related']:
            for related_term in item['related']:

                # process each related search term through each of the sources
                search_text = related_term
                for i, source in enumerate(sources):
                    flag = i == 0
                    matches = get_articles(search_text, source, threshold, adv_flag=flag)

                    # append any matches to the 'related_articles' key
                    these_matches['related_articles'] += matches

        # append matches for this item in the article_matches list
        article_matches.append(these_matches)

        # create path_out if it's not yet defined
        if not os.path.exists(path_out):
            os.makedirs(path_out)

        # define filepath for export, and delete it if it already exists
        filepath = os.path.join(path_out, 'eb_article_matches.json')
        if os.path.exists(filepath):
            os.remove(filepath)

        # export data
        with open(filepath, 'w') as file:
            file.write(json.dumps(article_matches, indent=2))

    # return matches
    return article_matches


# get a (flattened) list of all EB matches

def get_unique_articles(matches, path_out=None):
    # initialize list of all matches
    all_matches = []

    # iterate through matches, combining primary and related matches for each item
    for item in matches:
        these_matches = item['primary_articles'] + item['related_articles']

        # append matches for this item in the list of all matches
        all_matches += these_matches

    # define list of unique matches
    unique_matches = []
    [unique_matches.append(x) for x in all_matches if x not in unique_matches]

    # export data

    if not os.path.exists(path_out):
        os.makedirs(path_out)

    filepath = os.path.join(path_out, '../cache/eb_articles.json')
    if os.path.exists(filepath):
        os.remove(filepath)

    with open(filepath, 'w') as file:
        file.write(json.dumps(unique_matches, indent=2))

    return unique_matches
