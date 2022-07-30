from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.user import ns_user
from views.auth import ns_auth
from dao.model.user import User


def create_app(config_object):
    """Функция создания приложения"""
    application = Flask(__name__)
    application.config.from_object(config_object)
    register_extensions(application)
    application.app_context().push()
    return application


def register_extensions(app):
    """Функция регистрации настроек приложения"""
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(ns_user)
    api.add_namespace(ns_auth)
    # create_data(app, db)    # Раскомментировать для создания первоначальных пользователей


def create_data(app, db):
    """Функция создания первоначальных данных user в БД"""
    with app.app_context():
        db.create_all()

        u1 = User(username="vasya", password="my_little_pony", role="user")
        u2 = User(username="oleg", password="qwerty", role="user")
        u3 = User(username="oleg", password="P@ssw0rd", role="admin")

        with db.session.begin():
            db.session.add_all([u1, u2, u3])


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
