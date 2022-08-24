from app import db, ma

"""
Microgrid ESS table SQLALchemy ORM Class
"""

class MicrogridESSORM(db.Model):
    '''
    MicrogridESS class instantiated using the db.model
    '''
    __table__ = db.Model.metadata.tables['edison_dev.microgrid_ess']

class MicrogridESSORMSchema(ma.SQLAlchemySchema):
    """
    Marshmellow used to serialize microgrid_ess table 
    """
    class Meta:
        module = MicrogridESSORM # to return all the fields
        fields = ('id','created_time','ext_key','dt_connection','text_product_use','id_customer','id_microgrid','name_village','nbr_avg_solar_insolation_annual','nbr_base_load_kw','nbr_capacity_kw','nbr_storage_kwh','text_coordinates','id_rco','id_rto')

