from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate

from blog.article.views import article
from blog.auth.views import auth
from blog.database import db
from blog.user.views import user
from blog.views.authors import authors_app


login_manager = LoginManager()
app = Flask(__name__)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = ')c46i=c^-in+6v4^%cw$m11m5ubaz(3vob1ffcdysa5+t@+tdj'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"

    db.init_app(app)
    Migrate(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from blog.mymodels import User

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
    app.register_blueprint(auth)
    app.register_blueprint(authors_app, url_prefix="/authors")


@app.cli.command("create-tags")
def create_tags():
    """
    Run in your terminal:
    ➜ flask create-tags
    """
    from blog.mymodels import Tag

    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    print("created tags")
