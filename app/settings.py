from os import environ


class Settings(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SECRET_KEY = environ.get("SECRET_KEY")


class Development(Settings):
    DEBUG = False


class Prodaction(Settings):
    DEBUG = True
