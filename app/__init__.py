from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, Integer, func, Column, Integer, String, ForeignKey, text, Text
from flask_login import LoginManager

from app import models
from  .authors import authors

# class Base(DeclarativeBase):
#     pass

# db = SQLAlchemy(model_class=Base)

def create_app():    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Ssecret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/blog'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    login_manager_author = LoginManager()
    login_manager_author.login_view = 'authors.login'
    login_manager_author.init_app(app)

    @login_manager_author.user_loader
    def load_user(user_id):
        return models.AuthorAccounts.query.get(user_id)
    
    app.register_blueprint(authors)
    
    models.db.init_app(app)
    return app
