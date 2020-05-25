import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable
    to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer().with_variant(
        Integer, "sqlite"), primary_key=True)
    title = db.Column(db.String(80), unique=True)
    release_date = db.Column(db.DateTime, nullable=False)

    scenes_movie = db.relationship('Scene', backref='movies')

    def details(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer().with_variant(
        Integer, "sqlite"), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    age = db.Column(db.Integer().with_variant(
        Integer, "sqlite"), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    scenes_actor = db.relationship('Scene', backref='actors')

    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Scene(db.Model):
    __tablename__ = 'scenes'

    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movies.id'), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey(
        'actors.id'), primary_key=True)
    start_time = db.Column(db.String(25), nullable=False)
