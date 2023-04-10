from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import logout_user
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, static_folder='../static')


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template(
            'auth/login.html',
        )

    email = request.form.get('email')
    password = request.form.get('password')

    from blog.mymodels import User

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Check your login detais')
        return redirect(url_for('.login'))
    return redirect(url_for('user.profile', pk=user.id))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))
