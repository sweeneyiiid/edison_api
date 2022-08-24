from app import db, ma

"""
Microgrid Hourly table SQLALchemy ORM Class
"""

class MicrogridHourlyORM(db.Model):
    '''
    Microgrid Hourly class instantiated using the db.model
    '''
    __table__ = db.Model.metadata.tables['edison_dev.microgrid_hourly']

class MicrogridHourlyORMSchema(ma.SQLAlchemySchema):
    """
    Marshmellow used to serialize microgrid_ess table 
    """
    class Meta:
        module = MicrogridHourlyORM # to return all the fields
        fields = ('created_time','ext_key','dt_connection','text_product_use','id_customer','id_microgrid','name_village','nbr_avg_solar_insolation_annual','nbr_base_load_kw','nbr_capacity_kw','nbr_storage_kwh','text_coordinates','id_rco','id_rto')
