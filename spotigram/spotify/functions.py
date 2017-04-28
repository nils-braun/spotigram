import json

import requests

from getapy.basetypes import List, PageableObject, StrictParseObject
from spotigram.spotify.datatypes import Access, Device, Track, Artist, Playlist, SpotifyUser, PlaylistStub, Snapshot, \
    SpotifyPageableObject


def parse(r, parse_type=None):
    import getapy

    if parse_type:
        return getapy.parse(r.json(), parse_type)
    else:
        return r.text


def get_devices(access):
    class DeviceList(StrictParseObject):
        devices = List(Device)

    r = requests.get("https://api.spotify.com/v1/me/player/devices", headers=access.get_headers())
    return parse(r, DeviceList).devices


def search(query, access):
    class SearchResult(StrictParseObject):
        artists = PageableObject(Artist)
        tracks = PageableObject(Track)

    r = requests.get("https://api.spotify.com/v1/search", headers=access.get_headers(),
                     params={"query": query, "type": "artist,track"})

    return parse(r, SearchResult)


def play(playable_object, device, access):

    if isinstance(playable_object, list):
        data = json.dumps({
            "uris": [track.uri for track in playable_object],
        })
    else:
        data = json.dumps({
            "context_uri": playable_object.uri,
        })

    r = requests.put("https://api.spotify.com/v1/me/player/play",
                     headers=access.get_headers(),
                     data=data,
                     params={"device_id": device.id})

    return parse(r)


def authorize(client, state, scopes=None):
    # TODO: Do not do a get here
    if scopes is None:
        scopes = ["user-read-playback-state", "user-modify-playback-state streaming",
                  "playlist-modify-private", "playlist-read-private", "playlist-read-collaborative"]

    r = requests.get("https://accounts.spotify.com/authorize", params={
        "client_id": client.client_id,
        "response_type": "code",
        "state": state,
        "redirect_uri": client.url,
        "scope": " ".join(scopes)})
    return r.url


def tokenize(code, client):
    r = requests.post("https://accounts.spotify.com/api/token", data={
        "client_secret": client.client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client.client_id,
        "redirect_uri": client.url
    })

    return parse(r, Access)


def refresh_access(access, client):
    r = requests.post("https://accounts.spotify.com/api/token", data={
        "client_secret": client.client_secret,
        "grant_type": "refresh_token",
        "client_id": client.client_id,
        "refresh_token": access.refresh_token,
        "redirect_uri": client.url
    })

    new_access = parse(r, Access)
    new_access.refresh_token = access.refresh_token

    return new_access


def get_spotify_user(access):
    r = requests.get("https://api.spotify.com/v1/me",
                     headers=access.get_headers())

    return parse(r, SpotifyUser)


def create_playlist(title, spotify_user, access):
    data = json.dumps({"name": title, "public": False, "collaborative": False})

    r = requests.post("https://api.spotify.com/v1/users/{user_id}/playlists".format(user_id=spotify_user.id),
                      headers=access.get_headers(), data=data)

    return parse(r, Playlist)


def get_playlists(spotify_user, access):
    r = requests.get("https://api.spotify.com/v1/users/{user_id}/playlists".format(user_id=spotify_user.id),
                     headers=access.get_headers())
    return parse(r, SpotifyPageableObject(PlaylistStub))


def fill_playlist(playlist, spotify_user, access):
    r = requests.get(
        "https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}".format(user_id=spotify_user.id,
                                                                                    playlist_id=playlist.id),
        headers=access.get_headers())

    return parse(r, Playlist)


def add_songs(playlist, songs, spotify_user, access):
    r = requests.post(
        "https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks".format(user_id=spotify_user.id,
                                                                                           playlist_id=playlist.id),
        headers=access.get_headers(), params={"uris": ",".join([song.uri for song in songs])})

    return parse(r, Snapshot)


def add_album(playlist, artist, spotify_user, access):
    raise NotImplementedError


def add_playlist(playlist_to, playlist_from, spotify_user, access):
    raise NotImplementedError