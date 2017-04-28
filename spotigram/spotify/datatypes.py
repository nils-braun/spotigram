from getapy.basetypes import String, GreedyStringParseObject, PageableObject, Boolean, Int, \
    StrictParseObject
from spotigram import app

Id = String


class Client:
    def __init__(self, client_id, client_secret, url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url


client = Client(client_id=app.config.get("SPOTIFY_CLIENT_ID"),
                client_secret=app.config.get("SPOTIFY_CLIENT_SECRET"),
                url=app.config.get("SPOTIFY_URL"))


def SpotifyPageableObject(subclass_type):
    class SpotifyPageableObjectInstance(PageableObject(subclass_type)):
        href = String()
        limit = Int()
        next = String()
        offset = Int()
        previous = String()
        total = Int()

    return SpotifyPageableObjectInstance

# TODO: Copy whole definition


class Device(GreedyStringParseObject):
    name = String()


class Access(GreedyStringParseObject):
    token_type = String()
    access_token = String()

    def __init__(self, refresh_token=""):
        self.refresh_token = refresh_token

    @classmethod
    def construct_from_json(cls, json):
        instance = super().construct_from_json(json)

        # TODO: Date handling
        instance.scope = instance.scope.split()

        return instance

    def get_headers(self):
        return {"Authorization": self.token_type + " " + self.access_token}


class Track(GreedyStringParseObject):
    name = String()


class Artist(GreedyStringParseObject):
    name = String()


class PlaylistStub(GreedyStringParseObject):
    collaborative = String()
    id = Id()
    name = String()
    images = String()
    uri = String()


class SpotifyUser(GreedyStringParseObject):
    id = Id()


class PlaylistTrack(GreedyStringParseObject):
    added_by = SpotifyUser()
    track = Track()
    added_at = String()
    is_local = Boolean()


class Playlist(GreedyStringParseObject):
    tracks = SpotifyPageableObject(PlaylistTrack)


class Snapshot(StrictParseObject):
    snapshot_id = String()
