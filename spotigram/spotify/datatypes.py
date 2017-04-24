from spotigram import app
from spotigram.utilities.basetypes import RequestedObject, StrictRequestedObject, Dict, PageableObject, StrictDict


class Client:
    def __init__(self, client_id, client_secret, url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url


client = Client(client_id=app.config.get("SPOTIFY_CLIENT_ID"),
                client_secret=app.config.get("SPOTIFY_CLIENT_SECRET"),
                url=app.config.get("SPOTIFY_URL"))


class Device(RequestedObject):
    def stringify(self):
        return "{name}".format(**self.__dict__)


class Access(RequestedObject):
    def __init__(self, refresh_token=""):
        self.refresh_token = refresh_token

    def from_json(self, json):
        super().from_json(json)

        # TODO: Date handling
        self.scope = self.scope.split()

    def get_headers(self):
        return {"Authorization": self.token_type + " " + self.access_token}


class Track(RequestedObject):
    def stringify(self):
        return "{name}".format(**self.__dict__)


class Artist(RequestedObject):
    def stringify(self):
        return "{name}".format(**self.__dict__)


class NoneObject(RequestedObject):
    def stringify(self):
        return ""

    def from_request(self, r):
        pass


class PlaylistStub(RequestedObject):
    def __init__(self):
        self.collaborative = None
        self.id = None
        self.name = None
        self.images = None
        self.uri = None

    def stringify(self):
        return "{name}".format(**self.__dict__)


class PlaylistTrack(StrictDict):
    def __init__(self):
        super().__init__({"added_by": SpotifyUser(), "track": Track()})
        self.added_at = None
        self.is_local = None


class Playlist(Dict):
    def __init__(self):
        Dict.__init__(self, {"tracks": PageableObject(PlaylistTrack())})


class SpotifyUser(RequestedObject):
    def __init__(self):
        self.id = None

    def stringify(self):
        return "{id}".format(**self.__dict__)


class Snapshot(StrictRequestedObject):
    def stringify(self):
        return "{snapshot_id}".format(**self.__dict__)

    def __init__(self):
        self.snapshot_id = None
