import language_processing as lang_process
import parse_institutional_data as parse_data
import pandas as pd
import re
import nltk
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet as wn
import json
import os

from importlib import reload
reload(lang_process)
reload(parse_data)

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')


# clean up phenomenon and keyword phrases
# express 'color mixing: subtractive' as 'subtractive color mixing', etc.
# express 'motion: simple harmonic motion' as 'simple harmonic motion', etc.
# express 'motion: visual motion detection as 'visual motion detection'
# express 'this-that' and 'this/that' as 'this that'
# convert to lower case, remove apostrophes

def preprocess(phrase, kind):
    proc_phrase = phrase
    if kind == 'phenomenon':
        proc_phrase = proc_phrase.lower().replace("'", "")
        if ':' in phrase:
            split = re.split(': ', proc_phrase)
            reordered = ' '.join(split[::-1])
            double_word = r'\b(\w+)\s+\1\b'
            separated_double = r'\b(\w+)\s(\w+)\s+\1\b'
            doubles = re.search(double_word, reordered)
            separated_doubles = re.search(separated_double, reordered)
            if doubles:
                reordered = reordered.replace(doubles.group(), doubles.group().split()[0])
            if separated_doubles:
                reordered = reordered.replace(separated_doubles.group(),
                                              ' '.join(separated_doubles.group().split()[:2]))
            proc_phrase = reordered
        if any(x in phrase for x in ['-', '/']):
            split = re.split('-|/', proc_phrase)
            proc_phrase = ' '.join(split)
    elif kind == 'keyword':
        proc_phrase = proc_phrase.lower().replace("'", "")
        if any(x in phrase for x in ['/']):
            split = re.split('-|/', proc_phrase)
            proc_phrase = ' '.join(split)
    return proc_phrase


# work tokenize and get pos tags for each word in a phrase

def get_token_tags(phrase):
    words = word_tokenize(phrase)
    tags = pos_tag(words)
    return tags


# define related terms
# a term is a list of tuples
# choose possibly significant "subsets" of each term
# e.g. grab all nouns, grab all adjective-nouns

def get_related(phrase):
    adj_nouns = lang_process.get_adj_nouns(phrase)
    noun_nouns = lang_process.get_noun_noun(phrase)
    vb_nouns = lang_process.get_vb_nouns(phrase)
    nouns = lang_process.get_nouns(phrase)
    verbs = lang_process.get_verbs(phrase)
    adjectives = lang_process.get_adjectives(phrase)
    related_items = adj_nouns + nouns + noun_nouns + vb_nouns + verbs + adjectives
    related_items = [x for x in related_items if x]
    return related_items


# get wordnet synsets (name and definition) for each word in a phrase

def get_syns(phrase):
    this_phrase = []
    for word, pos in phrase:
        syns = wn.synsets(word)
        if not syns:
            continue
        syn_names = [syn.name() for syn in syns]
        syn_defs = [syn.definition() for syn in syns]
        this_word = {
            'word': (word, pos),
            'syns': syn_names,
            'defs': syn_defs
        }
        this_phrase.append(this_word)
    return this_phrase


def get_all_data(phrase):
    phrase = get_token_tags(phrase)
    data = {
        'primary': phrase,
        'related': get_related(phrase),
        'syns': get_syns(phrase)
    }
    return data
