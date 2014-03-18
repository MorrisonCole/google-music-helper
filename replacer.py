import logging
import authentication
import helper
import yes_no

logger = logging.getLogger('google-music-helper')

mobile_api = None
web_api = None


def init():
    global mobile_api, web_api

    mobile_api = authentication.get_mobile_api()
    web_api = authentication.get_web_api()


if __name__ == "__init__":
    init()


def find_and_replace_uploaded_albums(uploaded_songs):
    uploaded_albums = helper.get_uploaded_albums(uploaded_songs)

    for (album, artist) in uploaded_albums:
        print_uploaded_album_info((album, artist), uploaded_songs)

        query = album + " " + artist

        logger.log(logging.INFO, 'Searching All Access for: %s' % query)

        search_results = mobile_api.search_all_access(query)
        album_hits = search_results.get('album_hits', [''])

        if album_hits:
            print "All Access entry found!"

            # Take the first result, since they are sorted by confidence.
            album_hit = album_hits[0]

            album_name = album_hit['album']['name']
            album_id = album_hit['album']['albumId']

            print_album_info(album_id)

            question = "Replace with All Access version? (Your original uploaded tracks will be deleted)"
            replace = yes_no.query_yes_no(question, default="yes")

            if replace:
                print "Replacing with All Access entry:", album_name.decode('utf-8')
                replace_uploaded_album((album, artist), album_id, uploaded_songs)
        else:
            print "Could not find All Access entry"


def replace_uploaded_album((album, artist), album_id, uploaded_songs):
    for song in uploaded_songs:
        if (song['album'] == album) and (song['artist'] == artist):
            song_title = song['title']

            print "Deleting track:", song_title.decode('utf-8')

            song_id = song['id']
            web_api.delete_songs(song_id)

    add_tracks_from_album(album_id)


def add_tracks_from_album(album_id):
    album_info = mobile_api.get_album_info(album_id, include_tracks=True)

    for track in album_info["tracks"]:
        track_name = track["title"].encode('utf-8')
        track_id = track["nid"].encode('utf-8')

        print "Adding track:", track_name.decode('utf-8')
        mobile_api.add_aa_track(track_id)


def print_uploaded_album_info((album, artist), uploaded_songs):
    print "Original Album Info:"
    print "  Name:", album.decode('utf-8')
    print "  Artist:", artist.decode('utf-8')

    tracks = helper.get_tracks_from_uploaded_album((album, artist), uploaded_songs)
    for track in tracks:
        track_number = track['track_number']
        track_name = track['title']

        print "    Track %r: %s" % (track_number, track_name.decode('utf-8'))


def print_album_info(album_id):
    album_info = mobile_api.get_album_info(album_id, include_tracks=True)

    album_name = album_info['name']
    album_artist = album_info['artist']

    print "All Access Album Info:"
    print "  Name:", album_name.decode('utf-8')
    print "  Artist:", album_artist.decode('utf-8')

    for track in album_info['tracks']:
        track_number = track['trackNumber']
        track_name = track['title']

        print "    Track %r: %s" % (track_number, track_name.decode('utf-8'))