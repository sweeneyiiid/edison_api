from app import db, ma

"""
WH transaction table SQLALchemy Class
"""

class WHTransaction(db.Model):
    '''
    Esp class instantiated using the db.model
    '''
    __table__ = db.Model.metadata.tables['edison_dev.wh_transaction']

class WHTransactionSchema(ma.SQLAlchemySchema):
    """
    Marshmellow used to serialize customer table 
    """
    class Meta:
        module = WHTransaction # to return all the fields
        fields = ('created_time','ext_key','date_start','id_esp','nbr_amt_paid_zmw','nbr_centa_amp_limit_1','nbr_centa_amp_limit_2','nbr_centa_amp_limit_3','nbr_centa_amp_limit_4','nbr_centa_amp_limit_5','nbr_days_purchased','id_microgrid_ess','id_seller')
