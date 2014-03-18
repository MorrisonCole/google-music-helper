import os.path
import sys

from gmusicapi import Mobileclient, Musicmanager, Webclient

from google_music_helper import config, locations


def log_in():
    global username, password

    default_details_file = locations.WORK_DIRECTORY + 'authentication_details'

    if os.path.isfile(default_details_file):
        print "Using log in details from", default_details_file
        with open(default_details_file) as details_file:
            lines = details_file.readlines()
            username = lines[0]
            password = lines[1]
    else:
        print "You must provide your All Access account details..."
        username = raw_input("Username: ")
        password = raw_input("Password: ")


def setup_mobile_api():
    global mobile_api
    mobile_api = Mobileclient()

    mobile_logged_in = mobile_api.login(username, password)

    if not mobile_logged_in:
        print "Failed to log in to the mobile API, ensure your details are correct and try again."
        sys.exit(0)


def setup_web_api():
    global web_api
    web_api = Webclient()

    web_logged_in = web_api.login(username, password)

    if not web_logged_in:
        print "Failed to log in to the web API, ensure your details are correct and try again."
        sys.exit(0)


def setup_music_manager_api():
    global music_manager_api
    music_manager_api = Musicmanager()

    if not config.get_is_authenticated():
        print "Follow the instructions to authenticate with Google..."
        credentials = music_manager_api.perform_oauth()
        if credentials is not None:
            config.set_is_authenticated(True)
        else:
            print "Failed to authenticate, try again."
            sys.exit(0)

    music_manager_logged_in = music_manager_api.login()

    if not music_manager_logged_in:
        print "Failed to log in to the music manager API, you will be asked to authenticate again next run."

        sys.exit(0)


def get_mobile_api():
    return mobile_api


def get_web_api():
    return web_api


def get_music_manager_api():
    return music_manager_api