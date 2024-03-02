from sqlalchemy import (
    select,
    Integer,
    func,
    Column,
    Integer,
    String,
    ForeignKey,
    text,
    Text,
)

# from app import db
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class AuthorAccounts(UserMixin, db.Model):
    account_id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    def get_id(self):
        return self.account_id


class Authors(db.Model):
    author_id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    account_id = Column(Integer, ForeignKey(AuthorAccounts.account_id))


class Articles(db.Model):
    article_id = Column(Integer, primary_key=True)
    article_title = Column(Text, nullable=False)
    article_content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey(Authors.author_id))
    total_views = Column(Integer, default=0)
    article_photo = Column(Text, default='https://t3.ftcdn.net/jpg/02/48/42/64/360_F_248426448_NVKLywWqArG2ADUxDq6QprtIzsF82dMF.jpg')


class ReaderAccounts(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    username = Column(String(150))
    password = Column(String(100))
