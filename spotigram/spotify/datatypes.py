from spotigram import app
from spotigram.utilities.basetypes import RequestedObject


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
