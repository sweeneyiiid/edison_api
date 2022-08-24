import os
from dotenv import load_dotenv, find_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(find_dotenv())

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = True
    CSRF_ENABLED = True

"""
Multiple connection using bind https://stackoverflow.com/questions/33248702/flask-sqlalchemy-example-around-existing-database
"""
class Configdb(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('AWS_DB_URI_DEV') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = os.getenv('AWS_DB_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_BINDS = {'aws_dev': os.getenv('AWS_DB_URI')}

class ConfigMongo(object):
    CONNECTION_STRING = os.getenv('DEV_MONGO_DATABASE_URI')
    # CONNECTION_STRING = os.getenv('PROD_MONGO_DATABASE_URI')