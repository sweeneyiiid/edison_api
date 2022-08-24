"""
	Update products
	 - this is a manual process based on specs received from ESP
	 - copied process from insert_update_sandbox.py
"""	 

from app import db, ma
import datetime

#https://www.geeksforgeeks.org/md5-hash-python/
import hashlib as hb



"""
# migrating porperly https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date
# validation properly https://flask-marshmallow.readthedocs.io/en/latest/
# migration issues with existing table error https://stackoverflow.com/questions/51342994/how-does-one-resolve-a-table-already-exists-error-in-flask
# Query existing db aws connect with SQLAlchemy Best method: https://stackoverflow.com/questions/55083963/how-to-reflect-an-existing-table-by-using-flask-sqlalchemy
# Query Operations: https://docs.sqlalchemy.org/en/13/orm/tutorial.html#querying-with-joins
# Update Operations: https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information
# Update with orm: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#querying-records
"""

# from app.models.shs_ess.shs_ess_model import ShsEss, ShsEssSchema
# from app.models.shs_ess.payg_model import PayG, PayGSchema
from app.models.shs_ess.product_model import Product, ProductSchema

def update_insert_product(payload, table=Product, table_schema=ProductSchema):
    """
    This function creates a new ess in the shs table
    based on the passed in shs_ess payload
    :return:        201 on success, 406 on ess exists
    """
    id_esp = payload.get("id_esp")
    ext_key = payload.get("ext_key")
	#Need Ext key AND id_esp
	# https://stackoverflow.com/questions/3332991/sqlalchemy-filter-multiple-columns
    existing_rec = (
        table.query.filter(table.ext_key == ext_key, table.id_esp == id_esp).first()
    )

    if existing_rec is None:
        """
        If ess doesnt exist, create new one
        https://marshmallow.readthedocs.io/en/stable/quickstart.html
        Add created_by, created_time autofileds
        """

        # auto fields created by and time
        payload['created_by'] = "REEEP"
        payload['created_time'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        schema = table_schema()
        new_rec = schema.load(payload)

        db.session.add(new_rec)
        db.session.commit()

        # Serialize and return the newly created ess in the response
        # data = schema.dump(new_ess)
        # print(data)
        print('new product added')
        return 406
    else:
        """
        IF ess already exists, update existing ess
        TODO: detailed response message and mashmellow update format
        Add modified_by, modified_time autofileds
        """
        print('record already exists, not updated')
        # auto fields update for modified by and time
        # payload['modified_by'] = "REEEP"
        # payload['modified_time'] = datetime.datetime.utcnow()

        # table.query.filter(table.ext_key == ext_key).update(payload)
        # db.session.commit()
        # print("existing ess data updated")
        # return 200

# add a new record to shs_ess table
payload = {

    'id_tier':1,
    'name_product':'Check Product3',
    'nbr_lights':3,
    'nbr_wh_max':2,
    'nbr_wh_min':0,
    'nbr_wt_peak':6,
    'product_type':'SHS',
    'id_esp':3,
    'ext_key':'check product3',
    'verified':1,
}

#need ext_id to be unique id (not sure why)
payload['ext_id'] = hb.md5((str(payload['id_esp'])+payload['ext_key']).encode()).hexdigest()


# Quick way to add new record
# new_ess = ShsEss(**payload)
# db.session.add(new_ess)
# db.session.commit()

# Using an inser update function
update_insert_product(payload)


