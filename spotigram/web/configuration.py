from spotigram.web.models import ConfigurationItem
from spotigram import db


class Configuration:
    def __getitem__(self, item):
        item = ConfigurationItem.query.filter_by(key=item).first()

        if item:
            return item.value
        else:
            raise IndexError

    def __setitem__(self, key, value):
        config_item = ConfigurationItem.query.filter_by(key=key).first()

        if not config_item:
            config_item = ConfigurationItem(key, value)
            db.session.add(config_item)
        else:
            config_item.value = value
            db.session.merge(config_item)

        db.session.commit()


configuration = Configuration()