from google.cloud import language_v1

from collections import defaultdict
import json
import os

from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '../../../Keys/serene-gradient-366819-ab45f8eae1c8.json'

client = language_v1.LanguageServiceClient()
type_ = language_v1.Document.Type.PLAIN_TEXT
language = "en"
encoding_type = language_v1.EncodingType.UTF8


# define entity extraction function call

def get_entities(groupings, fields, path_in, path_out=None):

    entity_analysis = {}

    for grouping in groupings:

        units = defaultdict(dict)
        unit_entities = defaultdict(dict)

        # process all byline fields for this grouping, then all description fields, etc.
        for field in fields[grouping]:
            path = os.path.join(path_in, grouping, field)

            # ignore hidden files
            for file in os.listdir(path):
                these_entities = []
                if file.startswith('.'):
                    continue

                # get id of unit (e.g. exhibit or gallery) corresponding to file
                id = file.split('.')[0]

                # read text file into string: text_content
                file_path = os.path.join(path, file)
                with open(file_path, 'r') as infile:
                    text_content = infile.read()

                # define analyze_entities call
                document = {'content': text_content, 'type_': type_, 'language': language}
                response = client.analyze_entities(request={'document': document, 'encoding_type': encoding_type})

                # for each entitye: get name, type, and salience
                for entity in response.entities:
                    this_entity = {
                        'name': entity.name,
                        'type': language_v1.Entity.Type(entity.type_).name,
                        'salience': entity.salience,
                        'source': 'language_v1'
                    }
                    these_entities.append(this_entity)

                unit_entities[id].update({field: these_entities})

        for k, v in unit_entities.items():
            units.update({k: v})

        if path_out:
            if not os.path.exists(path_out):
                os.makedirs(path_out)

            filepath = os.path.join(path_out, grouping + '_raw.json')

            if os.path.exists(filepath):
                os.remove(filepath)

            with open(filepath, "w") as outfile:
                outfile.write(json.dumps(units, indent=2))

        entity_analysis.update({grouping: units})

    return entity_analysis
