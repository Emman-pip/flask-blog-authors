from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Account
from flask_login import login_user, logout_user

auth = Blueprint("auth", __name__)


# @auth.route("/login")
# def login():
#     return render_template("auth/login.html")

# @auth.route("/login", methods=["POST"])
# def login_post():
#     email = request.form.get('email')
#     password = request.form.get('password')

#     user = Account.query.filter_by(email=email).first()
    
#     if not user or not check_password_hash(user.password, password):
#         flash('Invalid credentials.')
#         return redirect(url_for('auth.login'))
    
#     login_user(user)
#     return redirect(url_for('pages.homeReaders'))

# TODO: Do the authentication stuff first then do the database itself.


@auth.route("/reader-signup")
def signup():
    return render_template("auth/signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    user = db.session.query(Account).filter_by(email=email).first()

    if user:
        print(user)
        flash("You already have an account.")
        return redirect(url_for("auth.signup"))

    db.session.add(
        Account(
            email=email,
            username=username,
            password=generate_password_hash(password, method="pbkdf2:sha1"),
            role='reader'
        )
    )
    db.session.commit()

    return redirect(url_for("authors.login"))

    # return render_template('auth/signup.html')
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))