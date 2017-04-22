import requests

from spotigram.telegram.datatypes import Update, BotDescription
from spotigram.utilities.basetypes import List


def parse_request(r, object_instance):
    json = r.json()
    try:
        object_instance.from_json(json["result"])

        return object_instance
    except:
        print(json)
        raise


def get_me(bot):
    r = requests.get("https://api.telegram.org/bot{token}/getMe".format(token=bot.token))

    return parse_request(r, BotDescription())


def get_updates(bot, offset, timeout):
    r = requests.get("https://api.telegram.org/bot{token}/getUpdates".format(token=bot.token),
                     params={"allowedUpdates": ["messages"], "offset": offset, "timeout": timeout})

    return parse_request(r, List(Update()))


def send_message(bot, chat, text):
    r = requests.get("https://api.telegram.org/bot{token}/sendMessage".format(token=bot.token),
                     params={"chat_id": chat.id, "text": text, "parse_mode": "HTML"})

    return r.text
