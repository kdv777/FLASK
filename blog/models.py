from flask_login import UserMixin
from sqlalchemy import LargeBinary, Column

from blog.app import db
from blog.security import flask_bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False, default="", server_default="")
    last_name = db.Column(db.String(120), unique=False, nullable=False, default="", server_default="")
    username = db.Column(db.String(80), unique=True)
    is_staff = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(256), unique=True,  default="")
    _password = Column(LargeBinary)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = flask_bcrypt.generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return flask_bcrypt.check_password_hash(self._password, password)
