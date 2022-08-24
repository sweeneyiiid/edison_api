from app import db, ma

"""
Microgrid table SQLALchemy ORM Class
"""

class MicrogridORM(db.Model):
    '''
    Microgrid class instantiated using the db.model
    '''
    __table__ = db.Model.metadata.tables['edison_dev.microgrid']

class MicrogridORMSchema(ma.SQLAlchemySchema):
    """
    Marshmellow used to serialize microgrid table 
    """
    class Meta:
        module = MicrogridORM # to return all the fields
        fields = ('id','created_time','dt_installation','name_city','name_province','name_village','nbr_avg_solar_insolation_annual','nbr_base_load_kw','nbr_capacity_kw','nbr_storage_kwh','text_coordinates','id_rco','id_rto')
