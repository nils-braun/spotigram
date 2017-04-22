from spotigram import app
from spotigram.utilities.basetypes import Dict, StrictRequestedObject, RequestedObject


class Bot:
    def __init__(self, token):
        self.token = token


bot = Bot(token=app.config.get("TELEGRAM_BOT_KEY"))


class BotDescription(RequestedObject):
    pass


class Update(Dict):
    def __init__(self):
        super().__init__({"message": Message()})

    def stringify(self):
        return self.message.stringify()


class User(StrictRequestedObject):
    def __init__(self):
        self.first_name = None
        self.id = None

    def stringify(self):
        return "{first_name} ({id})".format(first_name=self.first_name, id=self.id)


class Chat(StrictRequestedObject):
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.id = None
        self.type = None
        self.title = None
        self.username = None

    @property
    def name(self):
        if self.type == "private":
            if self.username:
                return self.username
            else:
                return self.first_name
        return self.type

    def stringify(self):
        return "{name} ({id})".format(name=self.name, id=self.id)


class Message(Dict):
    def __init__(self):
        super().__init__({"from": User(), "chat": Chat()})

    def stringify(self):
        return "{user}: {text}".format(user=self.__dict__["from"].stringify(), text=self.text)
