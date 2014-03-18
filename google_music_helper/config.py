import logging

from google_music_helper import json_utils, locations


logger = logging.getLogger('google_music_helper')

default_configuration_file = locations.WORK_DIRECTORY + 'config.json'


def get_is_authenticated():
    configuration = json_utils.load_json_from_file(default_configuration_file)
    authenticated = configuration.get('authenticated', False)

    return authenticated


def set_is_authenticated(is_authenticated):
    logger.log(logging.INFO, "Setting 'authenticated': %r" % is_authenticated)

    configuration = json_utils.load_json_from_file(default_configuration_file)
    configuration['authenticated'] = is_authenticated
    json_utils.save_json_to_file(configuration, default_configuration_file)