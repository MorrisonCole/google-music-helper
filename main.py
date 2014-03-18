import gmusicapi
from gmusicapi import Mobileclient
from gmusicapi import Musicmanager
from gmusicapi import Webclient

import json
from helper import get_library_artists, get_uploaded_albums

from json_utils import dump_json_to_file

# Login details
print "You must provide your All Access account details..."
username = raw_input("Username: ")
password = raw_input("Password: ")

mobile_api = Mobileclient()
mobile_logged_in = mobile_api.login(username, password)

music_manager_api = Musicmanager()
# If running for first time, uncomment this and follow the instructions in the console
# music_manager_api.perform_oauth()
music_manager_logged_in = music_manager_api.login()

web_api = Webclient()
web_logged_in = web_api.login(username, password)

songs = mobile_api.get_all_songs()

artistList = get_library_artists(songs)

# TODO: for testing only
artistList = [artistList[0]]

# 1. Get all (artist, albums) for which all songs lack storeIds.
# 2. Search and see if the album exists.
# 3. If it does, delete the original tracks and add the store ones.
# 4. If not, warn and leave be.

uploaded_songs = music_manager_api.get_uploaded_songs()

dump_json_to_file(uploaded_songs, 'uploaded_songs.txt')

uploaded_albums = get_uploaded_albums(uploaded_songs)


def find_and_replace_uploaded_albums():
    for (album, artist) in uploaded_albums[0:1]:
        print "Searching All Access for uploaded album... "
        print "  Title:", album.decode('utf-8')
        print "  Artist:", artist.decode('utf-8')

        query = album + " " + artist
        search_results = mobile_api.search_all_access(query)
        album_hits = search_results.get('album_hits', [''])

        if album_hits:
            print "  Found All Access entry with query: ", query

            # Take the first result, since they are sorted by confidence.
            album_hit = album_hits[0]

            album_name = album_hit['album']['name'].encode('utf-8')
            album_id = album_hit['album']['albumId'].encode('utf-8')

            print json.dumps(album_hit, indent=2)

            print "  Replacing with All Access entry:", album_name.decode('utf-8')
            replace_uploaded_album((album, artist), album_id)
        else:
            print "  Could not find All Access entry"


def replace_uploaded_album((album, artist), album_id):
    for song in uploaded_songs:
        if (song['album'] == album) and (song['artist'] == artist):
            song_id = song['id']
            web_api.delete_songs(song_id)

    add_tracks_from_album(album_id)

def add_tracks_from_album(album_id):
    album_info = mobile_api.get_album_info(album_id, include_tracks=True)

    for track in album_info["tracks"]:
        trackName = track["title"].encode('utf-8')
        trackId = track["nid"].encode('utf-8')

        print "    Adding track:", trackName.decode('utf-8')
        mobile_api.add_aa_track(trackId)


def add_all_tracks_from_artists():
    global artist, artistId, artist_info, album, albumName, albumId, album_info, track, trackName, trackId
    for (artist, artistId) in artistList:
        print "ARTIST:", artist.decode('utf-8'), "ID:", artistId.decode('utf-8')

        if artistId:
            try:
                artist_info = mobile_api.get_artist_info(artistId, include_albums=True)
            except gmusicapi.exceptions.CallFailure:
                print "Failed to get artist info for ID: ", artistId
                continue

            for album in artist_info["albums"]:
                albumName = album["name"].encode('utf-8')
                albumId = album["albumId"].encode('utf-8')

                print "  ALBUM: " + albumName.decode('utf-8')

                album_info = mobile_api.get_album_info(albumId, include_tracks=True)

                for track in album_info["tracks"]:
                    trackName = track["title"].encode('utf-8')
                    trackId = track["nid"].encode('utf-8')

                    print "    TRACK:", trackName.decode('utf-8')
                    mobile_api.add_aa_track(trackId)

find_and_replace_uploaded_albums()