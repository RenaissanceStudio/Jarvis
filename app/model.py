from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, uid):
        self.title = title
        self.author_id = uid

    def __repr__(self):
        return '<todo %r>' % self.title


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # 1 : N
    # Reverse the relationship by adding the 'author' filed to the `ToDo` Model
    # This field can be used to access User instead of 'author_id'.
    todo_items = db.relationship('Todo', backref='author', lazy='dynamic')

    # write-only property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)

    def __repr__(self):
        return '<user %r>' % self.username
