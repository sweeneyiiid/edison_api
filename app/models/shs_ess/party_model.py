from app import db, ma
from marshmallow_sqlalchemy import ModelSchema, SQLAlchemyAutoSchema 
from marshmallow import Schema, fields, EXCLUDE, INCLUDE, RAISE

"""
PARTY table SQLALchemy Class reflecting PARTY table in aws db
"""

class Party(db.Model):
    '''
    PARTY class instantiated using the db.model
    '''
    __table__ = db.Model.metadata.tables['edison_dev.party']

class PartySchema(ModelSchema):
    """
    Marshmellow used to serialize table 
    """
    class Meta:
        model = Party 
        load_instance = True
        sqla_session = db.session
        unknown = INCLUDE 