from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from spotigram.flask.views import add_views

app = Flask(__name__)
db = SQLAlchemy(app)

app.config.from_object('config')
add_views(app)

