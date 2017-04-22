from spotigram.spotify.datatypes import Access, client
from spotigram.spotify.functions import get_devices, search, play, authorize, refresh_access


def get_answer(query, user, db):
    if query == "devices":
        if not user.refresh_code:
            return "You have to authorize first."

        access = Access(refresh_token=user.refresh_code)
        access = refresh_access(access, client)

        devices = get_devices(access)
        return "<b>Devices:</b>\n" + devices.stringify()
    elif query.startswith("search "):
        if not user.refresh_code:
            return "You have to authorize first."

        access = Access(refresh_token=user.refresh_code)
        access = refresh_access(access, client)

        results = search(query[len("search "):], access)
        return results.stringify()
    elif query.startswith("set device "):
        if not user.refresh_code:
            return "You have to authorize first."

        access = Access(refresh_token=user.refresh_code)
        access = refresh_access(access, client)

        devices = get_devices(access)

        for device in devices:
            if device.name == query[len("set device "):]:
                user.chosen_device = device.id
                db.session.merge(user)
                db.session.commit()
                return "OK"

        return "Wrong Name"
    elif query.startswith("play_song "):
        if not user.refresh_code:
            return "You have to authorize first."

        access = Access(refresh_token=user.refresh_code)
        access = refresh_access(access, client)

        if not user.chosen_device:
            return "You have to choose a device first"

        devices = get_devices(access)

        chosen_device = None

        for device in devices:
            if device.id == user.chosen_device:
                chosen_device = device

        if not chosen_device:
            return "You chosen device is not longer valid"

        results = search(query[len("play_song "):], access)
        track = results["tracks"][0]

        play(track, chosen_device, access)

        return "OK"
    elif query == "authorize":
        if user.refresh_code:
            return "You are already authorized."

        return "<a href='{url}'>Click here</a>".format(url=authorize(client, user.id))

    return "Do not know command"
