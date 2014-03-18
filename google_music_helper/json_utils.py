import json
import logging

logger = logging.getLogger('google_music_helper')


def save_json_to_file(json_data, file_name):
    with open(file_name, 'w') as outfile:
        json.dump(json_data, outfile, sort_keys=True, indent=2)


def load_json_from_file(file_name):
    with open(file_name, 'a+') as json_file:
        try:
            data = json.load(json_file)
        except ValueError:
            logger.log(logging.DEBUG, "No existing JSON found!")
            data = {}

    return data