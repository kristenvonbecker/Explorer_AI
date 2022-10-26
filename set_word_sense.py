import re

import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
from language_processing import *
from datetime import datetime
import os
import json

# download wordnet corpus
nltk.download('wordnet')

# load data
# each term in raw_terms is a list of dicts, each dict representing a word in a search phrase
# dict keys: word, a list [text, pos]; syns and defs, lists obtained from the object wn.synsets(text)
with open('data/search_terms/terms_with_word_syns.json') as file:
    terms_raw = json.load(file)


# get the plaintext of a search phrase (term)
def get_text(phrase):
    text = ' '.join(word[0] for word in phrase)
    return text

# get the part of speech label for a word, and encode it for wn.synset() formatting
# this data is obtained from nltk.pos_tags(search_phrase)
def get_pos(word):
    tag = word[1]
    if tag.startswith('N'):
        label = 'n'
    elif tag.startswith('V'):
        label = 'v'
    elif tag.startswith('J'):
        label = 'a'
    elif tag.startswith('R'):
        label = 'r'
    else:
        label = 'z'
    return label

###########################################

# offer user option of changing the part of speech
def change_word(curr_word):
    usr_input = input('\nChange word (e.g. spelling)? (y/n): ')

    if usr_input == 'n':
        flag = False
        return curr_word, flag
    elif usr_input == 'y':
        flag = True
        return get_new_word(curr_word)
    else:
        return change_word(curr_word)


# prompt the user for the correct word
def get_new_word(curr_word):
    usr_input = input('\nEnter correct word (in lower-case) or EXIT to quit: ')
    valid_input_pattern = r'\w+'
    if usr_input == 'EXIT':
        save_quit()
    elif re.search(valid_input_pattern, usr_input):
        return confirm_word(usr_input, curr_word)
    else:
        get_new_word(curr_word)


# confirm the new word
def confirm_word(new_word, curr_word):
    confirm = input('\nCorrect name = {}? (y/n): '.format(new_word))

    if confirm == 'n':
        flag = False
        return get_new_word(curr_word), flag
    elif confirm == 'y':
        flag = True
        return new_word, flag
    else:
        confirm_word(new_word, curr_word)


# offer user option of changing the part of speech
def change_pos(curr_pos):
    usr_input = input('\nChange POS? (y/n): ')

    if usr_input == 'n':
        return curr_pos
    elif usr_input == 'y':
        return get_new_pos(curr_pos, flag=False)
    else:
        change_pos(curr_pos)


# prompt the user for the part of speech
# n = noun, v = verb, a = adjective, r = adverb, s = adj satellite
def get_new_pos(curr_pos, flag=False):
    usr_input = input('\nEnter correct POS (n, v, a, r, s) or EXIT to quit: ')
    valid_input = ['n', 'v', 'a', 'r', 's', 'EXIT', 'BACK']

    if usr_input not in valid_input:
        get_new_pos(curr_pos, flag)
    else:
        if usr_input == 'EXIT':
            save_quit()
        else:
            return confirm_pos(usr_input, curr_pos, flag)


# confirm the part of speech choice
def confirm_pos(new_pos, prev_pos, flag):
    confirm = input('\nCorrect POS = {}? (y/n): '.format(new_pos))

    if confirm == 'n':
        return get_new_pos(prev_pos, flag)
    elif confirm == 'y':
        this_word['pos'] = new_pos

        if flag:
            senses = print_sense_defs(new_pos)
            get_sense(new_pos, senses)
        return new_pos
    else:
        confirm_pos(new_pos, prev_pos, flag)


# print the indexed list of senses and their definitions
def print_sense_defs(pos):
    senses = syn_def_df[['syns', 'defs']][syn_def_df['pos'] == pos]
    num_syns = len(senses)

    print('\n---')
    if num_syns == 0:
        print('There are no senses for that POS')
    for i in range(num_syns):
        print(i, senses.iloc[i]['syns'], senses.iloc[i]['defs'])
    print('-'*3)

    return senses


# prompt the user for the correct sense number
def get_sense(pos, senses):
    num_syns = len(senses)
    usr_input = input('\nEnter the line number (0-{}) of the correct sense '.format(num_syns-1)
                      + 'or EXIT to quit or POS to change the POS: ')
    valid_inputs = ['EXIT', 'POS'] + [str(i) for i in range(num_syns)]

    if usr_input not in valid_inputs:
        if usr_input.isnumeric():
            print('\nValue out of range, try again.')
        else:
            print('\nWrong format, try again.')
        get_sense(pos, senses)
    elif usr_input in [str(i) for i in range(num_syns)]:
        confirm_sense(int(usr_input), pos, senses)
    elif usr_input == 'EXIT':
        save_quit()
    elif usr_input == 'POS':
        get_new_pos(pos, flag=True)


# confirm the choice of sense
def confirm_sense(ind, pos, senses):
    sense = senses.iloc[ind]['syns']
    defn = senses.iloc[ind]['defs']
    confirm = input('\nCorrect word sense = {} {}? (y/n): '.format(sense, defn))

    if confirm == 'n':
        get_sense(pos, senses)
    elif confirm == 'y':
        this_word['sense'] = sense
    else:
        confirm_sense(ind, pos, senses)


# (save and) quit
def save_quit():
    confirm = input('\nSave work? (y/n): ')

    if confirm == 'n':
        print('Changes not saved\n')
        quit()
    elif confirm == 'y':
        this_term.append(this_word)
        terms_labeled.append(this_term)

        path = 'data/search_terms/sense_labels'
        if not os.path.exists(path):
            os.makedirs(path)

        dt = datetime.now()
        dt_str = dt.strftime("%d-%m-%Y_%H%M%S")
        filepath = os.path.join(path, dt_str + '.json')
        with open(filepath, "w") as f:
            f.write(json.dumps(terms_labeled, indent=2))
        print('Changes saved in data/search_terms/<datetime>.json\n')
        quit()
    else:
        save_quit()


# retun pos tag for synsets item
def syn_pos(syn):
    return syn.split('.')[1]


# prompt user for starting index
def select_start():
    start_index = input('\nSelect the starting index (0, 1, 2, 3,...): ')

    if start_index in [str(i) for i in range(len(terms_raw))]:
        return int(start_index)
    else:
        select_start()

##########################################

terms_labeled = []

start_index = select_start()
reindexed_terms = terms_raw[start_index:] + terms_raw[:start_index]

counter = 0

for term in reindexed_terms:
    this_term = []
    this_phrase = get_text([word['word'] for word in term])
    for word in [word for word in term if word['syns']]:
        this_word = {
            'word': word['word'][0],
            'pos':  get_pos(word['word']),
            'sense': ''
        }

        print('\n\nIndex = {}'.format(start_index+counter))
        print('-' * 3)
        print('For the phrase: {}'.format(this_phrase))
        print('-' * (len(this_phrase)+16))
        print('Word = {}'.format(tuple(word['word'])))
        print('-' * 3)

        new_word, flag = change_word(word['word'][0])
        this_word['word'] = new_word

        if flag:
            synset = wn.synsets(new_word)
            syns = [syn.name() for syn in synset]
            defs = [syn.definition() for syn in synset]
        else:
            syns = word['syns']
            defs = word['defs']
        pos_filter = [syn_pos(syn) for syn in syns]
        syn_def = list(zip(pos_filter, syns, defs))
        syn_def_df = pd.DataFrame(syn_def, columns=['pos', 'syns', 'defs'])

        pos = get_pos(word['word'])
        pos = change_pos(pos)

        num_syns = print_sense_defs(pos)
        get_sense(pos, num_syns)

        this_term.append(this_word)
    counter += 1

    terms_labeled.append(this_term)
