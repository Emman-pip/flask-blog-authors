from flask import Flask
from flask_login import LoginManager

from app import auth, models, pages

from .authors import authors


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Ssecret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/blog"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    login_manager_author = LoginManager()
    login_manager_author.login_view = "authors.login"
    login_manager_author.init_app(app)

    @login_manager_author.user_loader
    def load_user(user_id):
        return models.Account.query.get(user_id)

    app.register_blueprint(authors)
    app.register_blueprint(pages.bp)
    app.register_blueprint(auth.auth)

    models.db.init_app(app)
    return app


