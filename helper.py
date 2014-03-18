def get_library_artists(songs):
    artists = list()

    for song in songs:
        artist = song["artist"].encode('utf-8')
        artist_id = song.get('artistId', [''])[0].encode('utf-8')

        if (artist, artist_id) not in artists:
            artists.append((artist, artist_id))

    artists.sort(key=lambda tup: tup[0].lower())

    return artists


def get_uploaded_albums(uploaded_songs):
    albums = list()

    for song in uploaded_songs:
        artist = song['artist'].encode('utf-8')
        album = song['album'].encode('utf-8')

        if (album, artist) not in albums:
            albums.append((album, artist))

    albums.sort(key=lambda tup: tup[0].lower())

    return albums


def get_tracks_from_uploaded_album((album, artist), uploaded_songs):
    tracks = list()

    for song in uploaded_songs:
        song_artist = song['artist'].encode('utf-8')
        song_album = song['album'].encode('utf-8')

        if (song_album == album) and (song_artist == artist):
            tracks.append(song)

    tracks.sort(key=lambda track: track['track_number'])

    return tracks