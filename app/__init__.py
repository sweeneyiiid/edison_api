from flask import Flask
from flask_restplus import Api, Resource
from app.config import Config, Configdb, ConfigMongo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # https://flask-migrate.readthedocs.io/en/latest/
from flask_marshmallow import Marshmallow

from flask_pymongo import pymongo
import os

application = Flask(__name__)
application.config.from_object(Config)
application.config.from_object(Configdb)
application.debug = True

"""
Hide model from view: https://github.com/noirbizarre/flask-restplus/issues/583
Swagger UI Themes: https://github.com/noirbizarre/flask-restplus/issues/130
"""
api = Api(
    application,
    version = "2.0", 
	title = "EDISON API - REEEP", 
	# description = "MICROGRID API to collect post data from ESP's"
	# description = "MICROGRID API to collect post data from ESP's <style>.models {display: none !important}</style>"
    description = "RESTful API built for the Energy Data and Intelligence System for Off-Grid Networks (EDISON). Edison is a platform for tracking, and verification of renewable energy and the offgrid-market. </br>\
        <a target='_parent' href='mailto:daniel.sweeney@reeep.org; saminu.salisu@reeep.org; ali.khabir@reeep.org'>Contact Developers</a>" ,
    )

"""
SQL ALchemy DB connection and migration (local)
https://stackoverflow.com/questions/55083963/how-to-reflect-an-existing-table-by-using-flask-sqlalchemy
https://stackoverflow.com/questions/41184835/flask-sqlalchemy-multiple-databases-and-binds
"""
db = SQLAlchemy(application)
db.Model.metadata.reflect(bind=db.engine,schema='edison_dev')
migrate = Migrate(application, db)


"""
Marchmallow setup for marshalling
"""
ma = Marshmallow(application)

"""
Mongo DB connection setup and connection
https://medium.com/@summerxialinqiao/connect-flask-app-to-mongodb-atlas-using-pymongo-328e119a7bd8
Currently connected to Dev on mongoatlas
"""
client = pymongo.MongoClient(ConfigMongo.CONNECTION_STRING)
