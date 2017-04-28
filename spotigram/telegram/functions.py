import requests

from getapy.basetypes import List
from spotigram.telegram.datatypes import Update, BotDescription

from getapy import parse


def parse_request(r, parse_type):
    try:
        return parse(r.json()["result"], parse_type)
    except Exception as e:
        print(r.json())
        raise


def get_me(bot):
    r = requests.get("https://api.telegram.org/bot{token}/getMe".format(token=bot.token))

    return parse_request(r, BotDescription)


def get_updates(bot, offset, timeout):
    r = requests.get("https://api.telegram.org/bot{token}/getUpdates".format(token=bot.token),
                     params={"allowedUpdates": ["messages"], "offset": offset, "timeout": timeout})

    return parse_request(r, List(Update))


def send_message(bot, chat, text):
    r = requests.get("https://api.telegram.org/bot{token}/sendMessage".format(token=bot.token),
                     params={"chat_id": chat.id, "text": text, "parse_mode": "HTML"})

    return r.text
