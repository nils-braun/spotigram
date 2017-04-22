import json

import requests

from spotigram.spotify.datatypes import Access, Device, Track, Artist
from spotigram.utilities.basetypes import List, Dict, PageableObject


def parse_request(r, object_instance=None):
    # TODO: Error handling

    if object_instance:
        json = r.json()
        try:
            object_instance.from_json(json)
        except:
            print(json)
            raise

        return object_instance


def get_devices(access):
    r = requests.get("https://api.spotify.com/v1/me/player/devices", headers=access.get_headers())
    return parse_request(r, Dict({"devices": List(Device())})).devices


def search(query, access):
    r = requests.get("https://api.spotify.com/v1/search", headers=access.get_headers(),
                     params={"query": query, "type": "artist,track"})

    return parse_request(r, Dict({
        "artists": PageableObject(Artist(), access),
        "tracks": PageableObject(Track(), access),
    }))


def play(title, device, access, from_album=False):
    if not from_album:
        data = json.dumps({"uris": [title.uri]})

    r = requests.put("https://api.spotify.com/v1/me/player/play",
                     headers=access.get_headers(),
                     data=data,
                     params={"device_id": device.id})

    return parse_request(r)


def authorize(client, state, scopes=None):
    # TODO: Do not get here
    if scopes is None:
        scopes = ["user-read-playback-state", "user-modify-playback-state streaming"]

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

    return parse_request(r, Access())


def refresh_access(access, client):
    r = requests.post("https://accounts.spotify.com/api/token", data={
        "client_secret": client.client_secret,
        "grant_type": "refresh_token",
        "client_id": client.client_id,
        "refresh_token": access.refresh_token,
        "redirect_uri": client.url
    })

    return parse_request(r, Access(access.refresh_token))
