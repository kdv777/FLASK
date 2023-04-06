from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from blog.article.views import article
from blog.auth.views import auth_app
from blog.user.views import user
from blog.security import flask_bcrypt

import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = ')c46i=c^-in+6v4^%cw$m11m5ubaz(3vob1ffcdysa5+t@+tdj'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"

    db.init_app(app)
    Migrate(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    flask_bcrypt.init_app(app)

    from blog.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.user_loader
    def unauthorized():
        return redirect(url_for('auth_login'))

    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(auth_app)


__all__ = [
    "create_app",
    "db",
]
