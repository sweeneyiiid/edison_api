from app import db, ma
from marshmallow_sqlalchemy import ModelSchema, SQLAlchemyAutoSchema
from marshmallow import Schema, fields, EXCLUDE, INCLUDE, RAISE

"""
Product table SQLALchemy Class reflecting Product table in aws db
"""

class Product(db.Model):
    '''
    Product class instantiated using the db.model
    '''
    __table__ = db.Model.metadata.tables['edison_dev.product']

class ProductSchema(ModelSchema):
    """
    Marshmellow used to serialize table 
    #this is crazy, but for some reason marshmallow is appartently
    #smart enough to know that 'true' in a payload means BIT == 1
    #even though SQLALchemy tries to make a BIT and integer,
    #which doesnt work
    """
	
	#https://marshmallow.readthedocs.io/en/stable/quickstart.html#required-fields
	#this is crazy, but for some reason marshmallow is appartently 
	#smart enough to know that 'true' in a payload means BIT == 1
	#even though SQLALchemy tries to make a BIT and integer, 
	#which doesnt work
    verified = fields.Boolean() # override bit type expectation from mysql
	
    class Meta:
        model = Product 
        load_instance = True
        sqla_session = db.session
        unknown = INCLUDE
