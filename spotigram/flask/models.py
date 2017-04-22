from spotigram import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    refresh_code = db.Column(db.String(100), default="")
    chosen_device = db.Column(db.String(100), default="")

    def __init__(self, id):
        self.id = id


class ConfigurationItem(db.Model):
    __tablename__ = 'config'
    key = db.Column(db.String(50), primary_key=True, nullable=False)
    value = db.Column(db.String(100), nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value


