import logging
import gmusicapi

from google_music_helper import helper, authentication, yes_no


logger = logging.getLogger('google_music_helper')

mobile_api = None
web_api = None
music_manager_api = None


def init():
    global mobile_api, web_api, music_manager_api

    mobile_api = authentication.get_mobile_api()
    web_api = authentication.get_web_api()
    music_manager_api = authentication.get_music_manager_api()


if __name__ == "__init__":
    init()


def add_all_tracks_from_existing_artists():
    warning = "WARNING: This will unconditionally add ALL tracks for ALL artists present in your existing library. " \
              + "Are you sure you want to continue?"
    response = yes_no.query_yes_no(warning, default="no")

    if not response:
        return

    songs = mobile_api.get_all_songs()
    artist_list = helper.get_library_artists(songs)

    for (artist, artistId) in artist_list:
        print "ARTIST:", artist.decode('utf-8'), "ID:", artistId.decode('utf-8')

        if artistId:
            try:
                artist_info = mobile_api.get_artist_info(artistId, include_albums=True)
            except gmusicapi.exceptions.CallFailure:
                logger.log(logging.DEBUG, "Failed to get artist info for ID %s" % artistId)
                continue

            for album in artist_info["albums"]:
                album_name = album["name"].encode('utf-8')
                album_id = album["albumId"].encode('utf-8')

                print "  ALBUM: " + album_name.decode('utf-8')

                album_info = mobile_api.get_album_info(album_id, include_tracks=True)

                for track in album_info["tracks"]:
                    track_name = track["title"].encode('utf-8')
                    track_id = track["nid"].encode('utf-8')

                    print "    TRACK:", track_name.decode('utf-8')
                    mobile_api.add_aa_track(track_id)
