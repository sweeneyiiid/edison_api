from app import db, ma

# migrating porperly https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date
# validation properly https://flask-marshmallow.readthedocs.io/en/latest/
# migration issues with existing table error https://stackoverflow.com/questions/51342994/how-does-one-resolve-a-table-already-exists-error-in-flask
# Query existing db aws connect with SQLAlchemy Best method: https://stackoverflow.com/questions/55083963/how-to-reflect-an-existing-table-by-using-flask-sqlalchemy
# Query Operations: https://docs.sqlalchemy.org/en/13/orm/tutorial.html#querying-with-joins
# Update Operations: https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information

# Using basemap: https://www.youtube.com/watch?v=UK57IHzSh8I
# Base = automap_base()
# Base.prepare(db.engine, reflect=True)
# Esp  = Base.classes.esp

from app.models.orm_microgrid_ess import MicrogridESSORM, MicrogridESSORMSchema
from app.models.orm_microgrid import MicrogridORM, MicrogridORMSchema
from app.models.orm_wh_transations import WHTransaction, WHTransactionSchema
from app.models.shs_ess.shs_ess_model import ShsEss, ShsEssSchema

# query all
# u = MicrogridESSORM.query.all()
# for i in u:
#     print(i.ext_key)

# u = ShsEss.query.all()
# for i in u:
#     print(i)


# add or update an shs_ess record AC1873390
# ess = ShsEss.query.filter_by(ext_key='AC1873390').first()
# ess.text_sub_product_use = "Test_Sub_Use"
# db.session.commit()

# print(ess.text_sub_product_use)


# join test
# join = db.session.query(MicrogridORM, MicrogridESSORM).filter(MicrogridORM.id == MicrogridESSORM.id_microgrid).all()
# join = db.session.query(MicrogridORM, MicrogridESSORM).filter(MicrogridORM.id == MicrogridESSORM.id_microgrid).all()
# for m, e in join:
#     print(m.ext_key)
#     print(e.ext_key)


# Microgrid > ESS
# join = MicrogridORM.query.join(MicrogridESSORM, MicrogridORM.id == MicrogridESSORM.id_microgrid).all()
# join_mg_ess = db.session.query(MicrogridORM, MicrogridESSORM).outerjoin(MicrogridESSORM, MicrogridORM.id == MicrogridESSORM.id_microgrid).all()
# for m in join_mg_ess:
#     if m[1]:
#         print(' MG {} > Customer:{}'.format(m[0].id, m[1].id_customer))


# ESS > WH Transactions
# join_ess_whtransaction = db.session.query(MicrogridESSORM, WHTransaction).outerjoin(WHTransaction, MicrogridESSORM.id == WHTransaction.id_microgrid_ess).all()
# for m in join_ess_whtransaction:
#     if m[1]:
#         print(' ESS {} > Payment:{}'.format(m[0].id, m[1].nbr_amt_paid_zmw))

