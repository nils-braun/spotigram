def add_views(app):
    from flask import request

    from spotigram.web.models import User
    from spotigram import db
    from spotigram.spotify.functions import tokenize
    from spotigram.spotify.datatypes import client
    from spotigram.utilities.functions import query_messages

    @app.route("/spotify/accept/", methods=["GET"])
    def accept():
        access = tokenize(request.args.get("code"), client)

        user = User.query.filter_by(id=request.args.get("state")).first()
        user.refresh_code = access.refresh_token

        db.session.merge(user)
        db.session.commit()

        return ""

    @app.route("/check", methods=["GET"])
    def check():
        try:
            query_messages()
            return "OK"
        except Exception as e:
            raise

    @app.route("/authorize", methods=["GET"])
    def authorize():
        from spotigram.spotify.functions import authorize

        user = User.query.first()

        if not user:
            user = User("1234")
            db.session.add(user)
            db.session.commit()

        return authorize(client, user.id)

    @app.route("/test", methods=["GET"])
    def test():
        from spotigram.spotify.datatypes import Access
        from spotigram.spotify.functions import refresh_access, add_songs, get_playlists, get_spotify_user, \
            fill_playlist, search, play, get_devices

        user = User.query.first()
        access = Access(refresh_token=user.refresh_code)
        access = refresh_access(access, client)

        spotify_user = get_spotify_user(access)

        playlists = get_playlists(spotify_user, access)
        playlist_stub = playlists[-3]

        playlist = fill_playlist(playlist_stub, spotify_user, access)

        return_string = str(playlist)

        query = search("Metallica", access)

        return_string += str(query.tracks)

        add_songs(playlist, [query.tracks[0]], spotify_user, access)

        playlist = fill_playlist(playlist_stub, spotify_user, access)

        return_string += str(playlist)

        devices = get_devices(access)

        play(playlist, devices[0], access)

        return return_string
