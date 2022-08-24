from app import db, ma
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields, EXCLUDE, INCLUDE, RAISE

"""
PAYG table SQLALchemy Class reflecting payg table in aws db
"""

class PayG(db.Model):
    '''
    PayG class instantiated using the db.model
    '''
    __table__ = db.Model.metadata.tables['edison_dev.payg']

class PayGSchema(ModelSchema):
    """
    Marshmellow used to serialize customer table 
    """
    class Meta:
        model = PayG
        load_instance = True
        sqla_session = db.session
        unknown = INCLUDE 

        # module = PayG # to return all the fields
        # fields = ('dt_acquisition','dt_paid_off','nbr_curr_days_outstanding','nbr_days_paid','nbr_days_to_pay','nbr_down_payment')
