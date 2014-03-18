def find_and_replace_uploaded_albums(mobile_api, uploaded_albums):
    for (album, artist) in uploaded_albums:
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

            print "  Replacing with All Access entry:", album_name.decode('utf-8')
            replace_uploaded_album((album, artist), album_id)
        else:
            print "  Could not find All Access entry"


def replace_uploaded_album(web_api, (album, artist), album_id, uploaded_songs):
    for song in uploaded_songs:
        if (song['album'] == album) and (song['artist'] == artist):
            song_id = song['id']
            web_api.delete_songs(song_id)

    add_tracks_from_album(album_id)


def add_tracks_from_album(mobile_api, album_id):
    album_info = mobile_api.get_album_info(album_id, include_tracks=True)

    for track in album_info["tracks"]:
        track_name = track["title"].encode('utf-8')
        track_id = track["nid"].encode('utf-8')

        print "Adding track:", track_name.decode('utf-8')
        mobile_api.add_aa_track(track_id)