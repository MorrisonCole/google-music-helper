import json

__author__ = 'morrison'


def dump_json_to_file(json_data, file_name):
    global outfile
    with open(file_name, 'w') as outfile:
        json.dump(json_data, outfile, sort_keys=True, indent=2)