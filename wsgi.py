import os

from werkzeug.security import generate_password_hash
from blog.app import create_app, db

app = create_app()

"""
# @app.cli.command("init-db")
# def init_db():
#     
#     Run in your terminal:
#     flask init-db
#     
#     db.create_all()
#     print("done!")



@app.cli.command("create-users")
def create_users():

    from blog.models import User

    db.session.add(
        User(email='name@email.com', password=generate_password_hash('123'))
    )
    db.session.commit()
"""


def create_admin():
    from blog.models import User

    admin= User(username="admin", is_staff=True)
    os.environ.get("ADMIN_PASSWORD") or "adminpass"
    db.session.add(admin)
    db.session.commit()
    print("created admin:", admin)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        debug=True,
    )
