from collections import Counter
import numpy as np
import json
import os


# define merge function
# merge on entity name
# salience = max(salience for each dupe entity name)
# type = from (type for each dupe entity name), choose the one with the smallest index in ordered_types

ordered_types = ['PERSON',
                 'DATE',
                 'ORGANIZATION',
                 'LOCATION',
                 'NUMBER',
                 'EVENT',
                 'CONSUMER_GOOD',
                 'WORK_OF_ART',
                 'OTHER']


def choose_type(types):
    for type in ordered_types:
        if type in types:
            return type


# flag that indicates a list contains duplicate entity names
def has_dupes(entities):
    names = [entity['name'] for entity in entities]
    return len(names) > len(list(set(names)))


def merge(entities):
    if not has_dupes(entities):
        return entities
    names = [entity['name'] for entity in entities]
    merged_entities = []
    for name, count in Counter(names).items():
        types = [entity['type'] for entity in entities if entity['name'] == name]
        saliences = [entity['salience'] for entity in entities if entity['name'] == name]
        this_entity = {}
        this_entity['name'] = name
        this_entity['salience'] = np.max(saliences)
        this_entity['type'] = choose_type(types)
        this_entity['source'] = 'merge'
        merged_entities.append(this_entity)
    return merged_entities


def merge_all(groupings, path_in, path_out=None):
    entities_merged = {}
    for grouping in groupings:
        in_filepath = os.path.join(path_in, grouping + '_raw.json')
        with open(in_filepath, 'r') as file:
            entities = json.load(file)
        for id in entities.keys():
            for field in entities[id].keys():
                merged_entities = merge(entities[id][field])
                entities[id][field] = merged_entities
        out_filepath = os.path.join(path_out, grouping + '_merged.json')
        with open(out_filepath, 'w') as file:
            file.write(json.dumps(entities, indent=2))
    entities_merged.update({grouping: entities})
    return entities_merged
