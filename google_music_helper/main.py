import logging
import os
import sys

import replacer
from google_music_helper.json_utils import save_json_to_file
from google_music_helper import authentication, locations, choose_function


def create_work_directories():
    work_directories = [locations.WORK_DIRECTORY, locations.LOG_DIRECTORY, locations.OUTPUT_DIRECTORY]

    for directory in work_directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def set_up_loggers():
    global logger

    logging.basicConfig(filename=locations.LOG_DIRECTORY + 'google_music_helper.log', level=logging.INFO)

    logger = logging.getLogger('google_music_helper')
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)


create_work_directories()
set_up_loggers()

authentication.log_in()

authentication.setup_mobile_api()
authentication.setup_web_api()
authentication.setup_music_manager_api()

mobile_api = authentication.get_mobile_api()
web_api = authentication.get_web_api()
music_manager_api = authentication.get_music_manager_api()

# TODO: Refactor
while True:
    question = "\nPlease choose a function:" \
               + "\n1. Find and replace uploaded albums with All Access versions" \
               + "\n2. Add all tracks from existing artists in library" \
               + "\n3. Write uploaded songs listing to file" \
               + "\n4. Write all songs listing to file" \
               + "\n5. Exit\n"
    intended_function = choose_function.query_intended_function(question, range(1, 6))

    if intended_function == 1:
        replacer.init()
        replacer.find_and_replace_uploaded_albums()
    elif intended_function == 2:
        sys.stdout.write("Not yet implemented!\n")
    elif intended_function == 3:
        uploaded_songs = music_manager_api.get_uploaded_songs()

        output_location = locations.OUTPUT_DIRECTORY + 'all_uploaded_songs.json'
        save_json_to_file(uploaded_songs, output_location)

        sys.stdout.write("Wrote all uploaded songs (JSON) to %s\n" % output_location)
    elif intended_function == 4:
        songs = mobile_api.get_all_songs()

        output_location = locations.OUTPUT_DIRECTORY + 'all_songs.json'
        save_json_to_file(songs, output_location)

        sys.stdout.write("Wrote all songs (JSON) to %s\n" % output_location)
    elif intended_function == 5:
        sys.stdout.write("Exiting!\n")
        sys.exit(1)

# def add_all_tracks_from_artists():
#     global artist, artistId, artist_info, album, albumName, albumId, album_info, track, trackName, trackId
#     for (artist, artistId) in artistList:
#         print "ARTIST:", artist.decode('utf-8'), "ID:", artistId.decode('utf-8')
#
#         if artistId:
#             try:
#                 artist_info = mobile_api.get_artist_info(artistId, include_albums=True)
#             except gmusicapi.exceptions.CallFailure:
#                 print "Failed to get artist info for ID: ", artistId
#                 continue
#
#             for album in artist_info["albums"]:
#                 albumName = album["name"].encode('utf-8')
#                 albumId = album["albumId"].encode('utf-8')
#
#                 print "  ALBUM: " + albumName.decode('utf-8')
#
#                 album_info = mobile_api.get_album_info(albumId, include_tracks=True)
#
#                 for track in album_info["tracks"]:
#                     trackName = track["title"].encode('utf-8')
#                     trackId = track["nid"].encode('utf-8')
#
#                     print "    TRACK:", trackName.decode('utf-8')
#                     mobile_api.add_aa_track(trackId)
#
#                     # find_and_replace_uploaded_albums()