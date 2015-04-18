from project import db
from project import bcrypt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class BlogPost(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    game = db.Column(db.LargeBinary, nullable=False)
    game_name = db.Column(db.String, nullable=False)
    game_location = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, title, game, game_name, author_id, game_location):
        self.title = title
        self.game = game
        self.game_name = game_name
        self.author_id = author_id
        self.game_location = game_location

    def __repr__(self):
        return '<title {}'.format(self.title)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    posts = relationship("BlogPost", backref="author")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<name {}'.format(self.name)


class Games(db.Model):

    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.LargeBinary, nullable=False)
    game_name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, game, game_name):
        self.game = game
        self.game_name = game_name

    def __repr__(self):
        return '<Game Name {}'.format(self.game)