import os
from datetime import datetime
import json
from collections import defaultdict


def default_val():
    return '3-14-2000_123456'


default = defaultdict(default_val)


def save_word_senses(path, num_terms):

    word_sense = [{}] * num_terms

    # load search terms
    search_terms_filepath = os.path.join(path, 'primary_with_syns.json')
    with open(search_terms_filepath, 'r') as infile:
        search_terms = json.load(infile)

    # iterate through files in containing word labels
    path_to_labels = os.path.join(path, 'sense_labels/')
    json_files = os.listdir(path_to_labels)
    for filename in json_files:

        # ignore empty files
        if filename.startswith('.'):
            continue

        # from filename, extract starting index and datetime stamp
        filename_parse = filename.split('_')
        start_ind = int(filename_parse[0])
        date_str = filename_parse[2]
        this_date = datetime.strptime(date_str, '%m-%d-%Y')
        time_str = filename_parse[3].split('.')[0]
        this_time = datetime.strptime(time_str, '%H%M%S').time()
        datetime_stamp = datetime.combine(this_date, this_time)

        # load file data
        filepath = os.path.join(path_to_labels, filename)
        with open(filepath, 'r') as infile:
            data = json.load(infile)

        # iterate through items in data
        for item in data:
            # index of item in data
            delta_ind = data.index(item)
            # absolute index of item (as in search_terms_with_syns)
            abs_ind = start_ind + delta_ind

            # 'primary' field of corresponding item in search_terms
            search_term_item = search_terms[abs_ind]
            primary_item = {'primary': search_term_item['primary']}

            record_exists = True if word_sense[abs_ind] else False  # is this needed?

            # timestamp of existing record, or 3/14/2022
            dt = datetime.strptime(word_sense[abs_ind].get('timestamp', '3-14-2000_123456'), '%m-%d-%Y_%H%M%S')

            # data from this file
            this_data = [{'word': subitem['word'], 'sense': subitem['sense']} for subitem in item]

            # repalce existing record if the data from this file is newer
            if datetime_stamp > dt:
                word_sense[abs_ind]['primary'] = primary_item['primary']
                word_sense[abs_ind]['data'] = this_data
                word_sense[abs_ind]['timestamp'] = datetime_stamp.strftime('%m-%d-%Y_%H%M%S')

    # save word_sense to disk and return it
    filepath_out = os.path.join(path, 'search_term_word_sense.json')

    if os.path.exists(filepath_out):
        os.remove(filepath_out)

    with open(filepath_out, 'w') as f:
        f.write(json.dumps(word_sense, indent=2))

    return word_sense

