from getapy.basetypes import GreedyStringParseObject, StrictParseObject, String
from spotigram import app


class Bot:
    def __init__(self, token):
        self.token = token


bot = Bot(token=app.config.get("TELEGRAM_BOT_KEY"))


class BotDescription(GreedyStringParseObject):
    pass


class Chat(StrictParseObject):
    first_name = String()
    last_name = String()
    id = String()
    type = String()
    title = String()
    username = String()

    @property
    def name(self):
        if self.type == "private":
            if self.username:
                return self.username
            else:
                return self.first_name
        return self.type


class Message(GreedyStringParseObject):
    chat = Chat()

    @classmethod
    def construct_from_json(cls, json):
        # Special handling because we can not call a class member "from" in python

        instance = super().construct_from_json(json)
        instance.__dict__["from_user"] = User.construct_from_json(json["from"])

        return instance


class Update(GreedyStringParseObject):
    message = Message()


class User(StrictParseObject):
    first_name = String()
    id = String()