import pandas as pd
import json
import os


def get_unit_names(path, grouping):
    filepath = os.path.join(path, grouping + '.json')
    with open(filepath, 'r') as infile:
        all_units = json.load(infile)
    units = [unit['id'] for unit in all_units]
    return units


def split_fields(path_in, path_out, grouping, fields):

    filepath = os.path.join(path_in, grouping + '.json')
    df = pd.read_json(filepath)

    for field in fields:

        screen = df[field] != ''
        data = df[['id', field]][screen]

        for i in range(len(data)):
            id = data['id'].iloc[i]

            path = os.path.join(path_out, grouping, field)
            if not os.path.exists(path):
                os.makedirs(path)

            filename = os.path.join(path, id + '.txt')
            with open(filename, 'w') as outfile:
                outfile.write(data[field].iloc[i])


def get_keywords(path, type):
    with open(path, 'r') as infile:
        items = json.load(infile)

    labels = [item[type] for item in items]
    labels = [x for sublist in labels for x in sublist]
    labels = list(set(labels))

    return labels
