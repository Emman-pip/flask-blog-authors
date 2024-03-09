from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
)
from .models import db, Account, Authors, Articles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os

from datetime import datetime


# class for file uploading
class ArticlePhoto(FlaskForm):
    photo = FileField(validators=[FileRequired()])


authors = Blueprint("authors", __name__)


@authors.route("/author-home")
@login_required
def home():
    if current_user.role != "author":
        return redirect(url_for("pages.home"))
    return render_template("home.html", name=current_user)


# TODO: delete
@authors.route("/author-options")
def options():
    return render_template("authors/options.html")


@authors.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("pages.home"))
    return render_template("authors/authorLogin.html")


@authors.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    user = Account().query.filter_by(email=email).first()

    if not user:
        flash("Invalid email")
        return redirect(url_for("authors.login"))

    if not check_password_hash(user.password, password):
        flash("Invalid password")
        return redirect(url_for("authors.login"))

    if user.role == "author":
        login_user(user)
        return redirect(url_for("authors.yourPosts"))
    elif user.role == "reader":
        login_user(user)
        return redirect(url_for("pages.home"))


@authors.route("/author-signup")
def signup():
    return render_template("authors/authorSignup.html")


@authors.route("/author-signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    authorEmail = Account.query.filter_by(email=email).first()
    authorUsername = Account.query.filter_by(username=username).first()

    if authorUsername or authorEmail:
        flash("Invalid email or username")
        return redirect(url_for("authors.signup"))

    authorAccount = Account(
        username=username,
        email=email,
        password=generate_password_hash(password, method="pbkdf2:sha1"),
        role="author",
    )

    db.session.add(authorAccount)
    db.session.commit()

    return redirect(url_for("authors.login"))


@authors.route("/your-posts")
@login_required
def yourPosts():
    if current_user.role != "author":
        return redirect("pages.home")
    user = Authors.query.filter_by(account_id=current_user.account_id).first()
    if not user:
        db.session.add(Authors(account_id=current_user.account_id, description="None"))
        db.session.commit()
    posts = Articles.query.filter_by(
        author_id=Authors.query.filter_by(account_id=current_user.account_id)
        .first()
        .author_id
    ).all()
    return render_template("authors/yourPosts.html", posts=posts)


@authors.route("/new-post")
@login_required
def newPosts():
    if current_user.role != "author":
        return redirect("pages.home")
    name = current_user.username
    form = ArticlePhoto()
    return render_template("authors/newPost.html", name=name, form=form)


@authors.route("/new-post", methods=["POST"])
def newPosts_post():
    photo = ArticlePhoto()

    # if not photo.validate_on_submit():
    #     flash('Please upload a file')
    #     return redirect(url_for('authors.newPosts'))

    photo_data = photo.photo.data
    title = request.form.get("title")
    content = request.form.get("content")

    user = Authors.query.filter_by(account_id=current_user.account_id).first()

    if user:
        author_id = user.author_id
    else:
        newAuthor = Authors(description="None", account_id=current_user.account_id)
        db.session.add(newAuthor)
        db.session.commit()
    photo_data.save(
        os.path.join("app/static/uploads", secure_filename(photo_data.filename))
    )

    article = Articles(
        article_title=title,
        article_content=content,
        author_id=Authors.query.filter_by(account_id=current_user.account_id)
        .first()
        .author_id,
        article_photo=os.path.join(
            "./static/uploads", secure_filename(photo_data.filename)
        ),
        date=datetime.now()
    )

    db.session.add(article)
    db.session.commit()

    return redirect(url_for("authors.yourPosts"))


@authors.route("/author-info")
@login_required
def authorInfo():
    if current_user.role != "author":
        return redirect("pages.home")
    desc = Authors.query.filter_by(account_id=current_user.account_id).first()
    return render_template("authors/authorInfo.html", desc=desc)


@authors.route("/author-info", methods=["POST"])
@login_required
def authorInfo_post():
    if current_user.role != "author":
        return redirect("pages.home")
    description = request.form.get("description")
    userCheck = Authors.query.filter_by(account_id=current_user.account_id).first()
    if userCheck != None:
        userCheck.description = description
        db.session.commit()
        return redirect(url_for("authors.authorInfo"))

    user = Authors(description=description, account_id=current_user.account_id)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("authors.authorInfo"))


@authors.route("/delete/<article_id>")
@login_required
def delete(article_id):
    if current_user.role != "author":
        return redirect("pages.home")
    article = Articles.query.filter_by(article_id=article_id).first()
    if not article:
        return "Failed to delete."
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("authors.yourPosts"))


@authors.route("/update/<article_id>")
@login_required
def update(article_id):
    if current_user.role != "author":
        return redirect("pages.home")
    article = Articles.query.filter_by(article_id=article_id).first()
    return render_template("authors/updateArticle.html", article=article)


@authors.route("/update/<article_id>", methods=["POST"])
def update_post(article_id):
    if current_user.role != "author":
        return redirect("pages.home")
    title = request.form.get("title")
    content = request.form.get("content")
    article = Articles.query.filter_by(article_id=article_id).first()

    if not article:
        return "Filed to update the article. try again later."

    article.article_title = title
    article.article_content = content
    db.session.commit()

    return redirect(url_for("authors.yourPosts"))


@authors.route("/logout-author")
@login_required
def logout():
    logout_user()
    return redirect(url_for("authors.login"))
