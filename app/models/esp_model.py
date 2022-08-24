from app import db, ma

"""
ESP table SQLALchemy Class reflecting user esp table in aws
"""

class Esp(db.Model):
    '''
    Esp class instantiated using the db.model
    '''
    __table__ = db.Model.metadata.tables['edison_dev.esp']

class EspSchema(ma.SQLAlchemySchema):
    """
    Marshmellow used to serialize customer table 
    """
    class Meta:
        module = Esp # to return all the fields
        fields = ('id','name_company','ext_id','text_api_token','text_notification_email')
