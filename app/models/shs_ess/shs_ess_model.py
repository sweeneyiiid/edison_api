from app import db, ma
from marshmallow_sqlalchemy import ModelSchema, SQLAlchemyAutoSchema #Usinf ModelSchema as oppose flask_mashmellow schema https://stackoverflow.com/questions/31891676/update-row-sqlalchemy-with-data-from-marshmallow
from marshmallow import Schema, fields, EXCLUDE, INCLUDE, RAISE


"""
SHS_ESS table SQLALchemy Class reflecting shs_ess table in aws db
https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
"""

class ShsEss(db.Model):
    '''
    ShsEss class instantiated using the db.model
    https://stackoverflow.com/questions/7679893/how-to-override-a-column-name-in-sqlalchemy-using-reflection-and-descriptive-syn
    Foreign key: https://stackoverflow.com/questions/24872541/could-not-assemble-any-primary-key-columns-for-mapped-table
    '''
    __table__ = db.Model.metadata.tables['edison_dev.shs_ess']
    # __tablename__ = db.Model.metadata.tables['edison_dev.shs_ess']
    # __table_args__ = (
    #     db.PrimaryKeyConstraint('id_product', 'id_customer'),
    # )


    # add automated models
    # created_by = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    # created_by = db.Column(db.String)

    # def set_created_by(self):
    #     return self.created_by


class ShsEssSchema(ModelSchema):
    """
    Marshmellow used to serialize customer table 
    https://stackoverflow.com/questions/31891676/update-row-sqlalchemy-with-data-from-marshmallow
    Unknown keys exclude: https://marshmallow.readthedocs.io/en/stable/upgrading.html#schemas-raise-validationerror-when-deserializing-data-with-unknown-keys
    https://stackoverflow.com/questions/54391524/sqlalchemy-property-causes-unknown-field-error-in-marshmallow-with-dump-only
    """
    class Meta:
        model = ShsEss 
        load_instance = True
        sqla_session = db.session
        unknown = INCLUDE