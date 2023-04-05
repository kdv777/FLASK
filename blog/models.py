from flask_login import UserMixin

from blog.app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256))
    password = db.Column(db.String(256))
