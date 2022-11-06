import re
# import language_processing
import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
from datetime import datetime
import os
import json

# nltk.download('wordnet');


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

# prompt the user to request new phrase or exit

def get_next_phrase(start_index, curr_index):
    usr_input = input('\nProcess next phrase? ')
    if usr_input == 'y':
        pass
    elif usr_input == 'n':
        save_quit(start_index, curr_index)
    else:
        get_next_phrase(start_index, curr_index)


# offer user option of changing the word (e.g. spelling)
def change_word(curr_word):
    usr_input = input('\nChange word? ')
    flag = False
    if usr_input == 'n':
        return curr_word, flag
    elif usr_input == 'y':
        flag = True
        return get_new_word(curr_word), flag
    else:
        return change_word(curr_word)


# prompt the user for the correct word
def get_new_word(curr_word):
    usr_input = input('\nEnter correct word (in lower-case): ')
    valid_input_pattern = r'\w+'
    if re.search(valid_input_pattern, usr_input):
        return confirm_word(usr_input, curr_word)
    else:
        get_new_word(curr_word)


# confirm the new word
def confirm_word(new_word, curr_word):
    confirm = input('\nCorrect name = {}? '.format(new_word))
    if confirm == 'n':
        return get_new_word(curr_word)
    elif confirm == 'y':
        return new_word
    else:
        confirm_word(new_word, curr_word)


# offer user option of changing the part of speech
def change_pos(curr_pos):
    usr_input = input('\nChange POS? ')
    if usr_input == 'n':
        return curr_pos
    elif usr_input == 'y':
        return get_new_pos(curr_pos, flag=False)
    else:
        change_pos(curr_pos)


# prompt the user for the part of speech
# n = noun, v = verb, a = adjective, r = adverb, s = adj satellite
def get_new_pos(curr_pos, flag=False):
    usr_input = input('\nEnter correct POS (n, v, a, r, s): ')
    valid_input = ['n', 'v', 'a', 'r', 's']
    if usr_input in valid_input:
        return confirm_pos(usr_input, curr_pos, flag)
    else:
        get_new_pos(curr_pos, flag)


# confirm the part of speech choice
def confirm_pos(new_pos, prev_pos, flag):
    confirm = input('\nCorrect POS = {}? '.format(new_pos))
    if confirm == 'n':
        return get_new_pos(prev_pos, flag)
    elif confirm == 'y':
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
    usr_input = input('\nEnter the line number (0-{}) of the correct sense '.format(num_syns - 1)
                      + 'or pos to change the POS: ')
    valid_inputs = [str(i) for i in range(num_syns)]
    if usr_input == 'pos':
        get_new_pos(pos, flag=True)
    elif usr_input in valid_inputs:
        confirm_sense(int(usr_input), pos, senses)
    else:
        if usr_input.isnumeric():
            print('\nValue out of range, try again.')
        else:
            print('\nWrong format, try again.')
        get_sense(pos, senses)


# confirm the choice of sense
def confirm_sense(ind, pos, senses):
    sense = senses.iloc[ind]['syns']
    defn = senses.iloc[ind]['defs']
    confirm = input('\nCorrect word sense = {} {}? '.format(sense, defn))

    if confirm == 'n':
        get_sense(pos, senses)
    elif confirm == 'y':
        this_word['sense'] = sense
    else:
        confirm_sense(ind, pos, senses)


# (save and) quit
def save_quit(start_index, end_index):
    confirm = input('\nSave work? ')

    if confirm == 'n':
        print('Changes not saved\n')
        quit()
    elif confirm == 'y':
        this_term.append(this_word)
        terms_labeled.append(this_term)

        path = '../../cache/sense_labels/'
        if not os.path.exists(path):
            os.makedirs(path)

        dt = datetime.now()
        dt_str = dt.strftime("%m-%d-%Y_%H%M%S")
        filename = '_'.join([str(start_index), str(end_index), dt_str])
        filepath = os.path.join(path, filename + '.json')
        with open(filepath, "w") as f:
            f.write(json.dumps(terms_labeled, indent=2))
        print('Changes saved\n')
        quit()
    else:
        save_quit()


# retun pos tag for synsets item
def syn_pos(syn):
    return syn.split('.')[1]


# prompt user for starting index
def select_start():
    start_index = input('\nSelect the starting index: ')
    if start_index in [str(i) for i in range(len(terms_raw))]:
        return int(start_index)
    else:
        select_start()

##########################################


# load data
# each term in raw_terms is a dict representing a search phrase
# dict key: value pairs --
# primary: list of tuples
# related: list of lists of tuples
# syns: list of dicts -- each dict has the following keys: word, syns, defs

with open('../../cache/primary_with_syns.json') as file:
    terms_raw = json.load(file)

terms_labeled = []

start_index = select_start()
reindexed_terms = terms_raw[start_index:] + terms_raw[:start_index]

index_ctr = 0

for term in reindexed_terms:
    this_term = []
    phrase = term['primary']
    this_phrase = get_text(phrase)
    num_words = len(term['syns'])
    for item in term['syns']:
        this_word = {
            'orig_word': get_text([item['word']]),
            'sense': ''
        }
        print('\n\nIndex = {}'.format(start_index + index_ctr))
        print('-' * 3)
        print('For the phrase: {}'.format(this_phrase))
        print('-' * (len(this_phrase) + 16))
        print('Word = {}'.format(tuple(item['word'])))
        print('-' * 3)

        # this_word['orig_word'] = item['word'][0]
        new_word, flag = change_word(item['word'][0])

        if flag:
            synset = wn.synsets(new_word)
            syns = [syn.name() for syn in synset]
            defs = [syn.definition() for syn in synset]
        else:
            syns = item['syns']
            defs = item['defs']

        pos_filter = [syn_pos(syn) for syn in syns]
        syn_def = list(zip(pos_filter, syns, defs))
        syn_def_df = pd.DataFrame(syn_def, columns=['pos', 'syns', 'defs'])

        pos = get_pos(item['word'])
        pos = change_pos(pos)

        senses = print_sense_defs(pos)
        get_sense(pos, senses)

        this_term.append(this_word)
    get_next_phrase(start_index, start_index + index_ctr)
    index_ctr += 1

    terms_labeled.append(this_term)
