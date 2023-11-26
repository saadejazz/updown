from flask_login import UserMixin
from . import db
import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class File(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    timestamp = db.Column(db.DateTime, default = datetime.datetime.utcnow)
