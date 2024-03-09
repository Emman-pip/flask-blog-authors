from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func, text
from app.models import db, Articles, Authors, Account
from flask_login import current_user
from markupsafe import escape

bp = Blueprint("pages", __name__)


@bp.route("/")
@bp.route("/home")
def home():
    data = db.session.execute(
        text(
            "SELECT a.article_id, a.article_title, a.article_content, acc.username FROM articles AS a INNER JOIN authors ON authors.author_id=a.author_id INNER JOIN account AS acc ON acc.account_id=authors.account_id;"
        )
    )
    return render_template("pages/home.html", name=current_user, data=data)


# TODO: Add views and limits to queries, options to load more kasi what if super dami ng blog posts?
@bp.route("/article/<article_id>")
def article(article_id):
    data = Articles.query.filter_by(article_id=article_id).first()
    authorData = db.session.execute(
        text(
            f"SELECT authA.username, auth.description FROM articles INNER JOIN authors as auth ON articles.author_id=auth.author_id INNER JOIN account as authA ON auth.account_id=authA.account_id WHERE articles.article_id={escape(article_id)};"
        )
    )
    return render_template(
        "pages/article.html", data=data, author=authorData.fetchone()
    )
