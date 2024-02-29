from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from .models import db, AuthorAccounts, Authors, Articles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user


authors = Blueprint("authors", __name__)


@authors.route("/")
def home():
    return render_template('home.html',  name=current_user)


@authors.route("/author-options")
def options():
    return render_template("authors/options.html")


@authors.route("/author-login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('authors.yourPosts'))
    return render_template("authors/authorLogin.html")


@authors.route('/author-login', methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    author = AuthorAccounts().query.filter_by(email=email).first()
    
    if not author:
        flash('Invalid email')
        return redirect(url_for('authors.login'))
    
    if not check_password_hash(author.password, password):
        flash('Invalid password')
        return redirect(url_for('authors.login'))

    
    login_user(author)
    return redirect(url_for('authors.yourPosts'))


@authors.route("/author-signup")
def signup():
    return render_template("authors/authorSignup.html")


@authors.route("/author-signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    authorEmail = AuthorAccounts.query.filter_by(email=email).first()
    authorUsername = AuthorAccounts.query.filter_by(username=username).first()

    if authorUsername or authorEmail:
        flash("Invalid email or username")
        return redirect(url_for("authors.signup"))

    authorAccount = AuthorAccounts(
        username=username,
        email=email,
        password=generate_password_hash(password, method="pbkdf2:sha1"),
    )

    db.session.add(authorAccount)
    db.session.commit()

    return redirect(url_for("authors.login"))

@authors.route('/your-posts')
@login_required
def yourPosts():
    posts = Articles.query.filter_by(author_id=Authors.query.filter_by(account_id=current_user.account_id).first().author_id).all()
    return render_template('authors/yourPosts.html', posts=posts)
    # TODO: ADD UPDATE AND DELETE OPTIONS HERE


@authors.route('/new-post')
@login_required
def newPosts():
    name = current_user.username
    return render_template('authors/newPost.html', name=name)


@authors.route('/new-post', methods=["POST"])
def newPosts_post():
    title = request.form.get('title')
    content = request.form.get('content')
    
    user = Authors.query.filter_by(account_id = current_user.account_id).first()
    
    if user:
        author_id = user.author_id
    else:
        newAuthor = Authors(description='None', account_id=current_user.account_id)
        db.session.add(newAuthor)
        db.session.commit()
    article = Articles(article_title=title, article_content=content, author_id=Authors.query.filter_by(account_id=current_user.account_id).first().author_id)
    
    db.session.add(article)
    db.session.commit()
    
    return redirect(url_for('authors.yourPosts'))


@authors.route('/author-info')
@login_required
def authorInfo():
    desc = Authors.query.filter_by(account_id=current_user.account_id).first()
    return render_template('authors/authorInfo.html', desc=desc)



@authors.route('/author-info', methods=["POST"])
def authorInfo_post():
    description = request.form.get('description')
    userCheck = Authors.query.filter_by(account_id=current_user.account_id).first()
    if userCheck != None:
        userCheck.description = description
        db.session.commit()
        return redirect(url_for('authors.authorInfo'))
    
    user = Authors(description=description, account_id=current_user.account_id)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('authors.authorInfo'))
            
@authors.route('/delete/<article_id>')
@login_required
def delete(article_id):
    article = Articles.query.filter_by(article_id=article_id).first()
    if not article:
        return 'Failed to delete.'
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('authors.yourPosts'))

@authors.route('/update/<article_id>')
@login_required
def update(article_id):
    article = Articles.query.filter_by(article_id=article_id).first()
    return render_template('authors/updateArticle.html', article=article)


@authors.route('/update/<article_id>', methods=["POST"])
def update_post(article_id):
    title = request.form.get('title')
    content = request.form.get('content')
    article = Articles.query.filter_by(article_id=article_id).first()
    
    if not article:
        return 'Filed to update the article. try again later.'
    
    article.article_title = title
    article.article_content = content
    db.session.commit()
    
    return redirect(url_for('authors.yourPosts'))

    
@authors.route('/logout-author')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authors.login'))