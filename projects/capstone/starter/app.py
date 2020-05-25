import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

from models import db_drop_and_create_all, setup_db, Movie, Actor, Scene
from auth import AuthError, requires_auth

from datetime import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """ uncomment at the first time running the app """
    # db_drop_and_create_all()

    @app.route('/', methods=['GET'])
    def hi():

        return "hello world"

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(pyload):
        try:
            actors = Actor.query.all()
            formatted_actors = [actor.details() for actor in actors]
            return jsonify({
                'success': True,
                'actors': formatted_actors
            }), 200
        except:
            abort(500)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(pyload):
        try:
            movies = Movie.query.all()
            formatted_movies = [movie.details() for movie in movies]
            return jsonify({
                'success': True,
                'movies': formatted_movies
            }), 200
        except:
            abort(500)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_specific_actor(pyload, id):
        try:
            actor = Actor.query.filter_by(id=id).first()
            formatted_actor = actor.details()
            actor.delete()
            return jsonify({
                'success': True,
                'deleted_actor': formatted_actor
            }), 200
        except:
            abort(404)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_specific_movie(pyload, id):
        try:
            movie = Movie.query.filter_by(id=id).first()
            formatted_movie = movie.details()
            movie.delete()
            return jsonify({
                'success': True,
                'deleted_movie': formatted_movie
            }), 200
        except:
            abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_new_actor(pyload):
        data = request.get_json()

        print(data)

        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            formatted_actor = actor.details()

            return jsonify({
                'success': True,
                'new_actor': formatted_actor
            }), 200
        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_new_movie(pyload):
        data = request.get_json()

        print(data)

        title = data.get('title')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')

        try:
            release_date = datetime(year=year, month=month, day=day)
            movie = Movie(title=title, release_date=release_date)
            movie.insert()

            formatted_movie = movie.details()

            return jsonify({
                'success': True,
                'new_movie': formatted_movie
            }), 200
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def modify_specific_actor(pyload, id):
        data = request.get_json()

        print(data)

        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        actor = Actor.query.filter_by(id=id).first()

        if name:
            actor.name = name
        if age:
            actor.age = age
        if gender:
            actor.gender = gender

        try:
            actor.update()

            formatted_actor = actor.details()

            return jsonify({
                'success': True,
                'modified_actor': formatted_actor
            }), 200
        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def modify_specific_movie(pyload, id):
        data = request.get_json()

        print(data)

        title = data.get('title', None)
        year = data.get('year', None)
        month = data.get('month', None)
        day = data.get('day', None)

        movie = Movie.query.filter_by(id=id).first()
        release_date = movie.release_date
        print("release_date:", release_date)

        if title:
            movie.title = title
        if year:
            movie.release_date = release_date.replace(year=year)
        if month:
            movie.release_date = release_date.replace(month=month)
        if day:
            movie.release_date = release_date.replace(day=day)

        try:
            movie.update()

            formatted_movie = movie.details()

            return jsonify({
                'success': True,
                'modified_movie': formatted_movie
            }), 200
        except:
            abort(422)

    # ................................................ Error handling ................................................

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    @app.errorhandler(AuthError)
    def Auth_Error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error['description']
        }), e.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
