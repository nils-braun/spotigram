from spotigram import db
from spotigram.telegram.datatypes import bot
from spotigram.web.models import User
from spotigram.web.configuration import configuration
from spotigram.telegram.functions import get_updates, send_message
from spotigram.telegram.queries import get_answer


def query_messages():
    updates = get_updates(bot, timeout=10, offset=int(configuration["offset"]) + 1)

    for update in updates:
        message = update.message
        chat = message.chat
        query = message.text

        configuration["offset"] = str(update.update_id)

        telegram_id = message["from"].id
        user = User.query.filter_by(id=telegram_id).first()

        if not user:
            user = User(id=telegram_id)
            db.session.add(user)
            db.session.commit()

        content = get_answer(query, user, db)
        send_message(bot, chat, content)


def prepare_db():
    db.create_all()

    if "offset" not in configuration:
        configuration["offset"] = "0"
