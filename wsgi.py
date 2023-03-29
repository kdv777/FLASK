from werkzeug.security import generate_password_hash
from blog.app import create_app, db

app = create_app()


@app.cli.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    from blog.models import User

    db.session.add(
        User(email='name@email.com', password=generate_password_hash('123'))
    )
    db.session.commit()


#
# if __name__ == '__main__':
#     app.run(
#         host="0.0.0.0",
#         debug=True,
#     )
