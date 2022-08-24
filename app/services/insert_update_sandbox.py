from app import db, ma
import datetime

from app.utils.core import map_rekey, rename_keys

"""
# migrating porperly https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date
# validation properly https://flask-marshmallow.readthedocs.io/en/latest/
# migration issues with existing table error https://stackoverflow.com/questions/51342994/how-does-one-resolve-a-table-already-exists-error-in-flask
# Query existing db aws connect with SQLAlchemy Best method: https://stackoverflow.com/questions/55083963/how-to-reflect-an-existing-table-by-using-flask-sqlalchemy
# Query Operations: https://docs.sqlalchemy.org/en/13/orm/tutorial.html#querying-with-joins
# Update Operations: https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information
# Update with orm: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#querying-records
"""
from app.models.shs_ess.shs_ess_model import ShsEss, ShsEssSchema
from app.models.shs_ess.payg_model import PayG, PayGSchema


from app.services.shs_ess_wrapper import ShsEssWrapper


def update_insert_ess_shs(payload, table, table_schema, key):
    """
    This function creates a new update in the specified table based on the parameters
    payload: dictionary: json data to insert_update
    table : db.model: table object
    table_schema: db.model: schema
    key: string : key to use for search and update
    :return:        201 on success, 406 on ess exists
    TODO:match ext_key and id_esp
    """
    ext_key = payload.get(key)

    existing_ess = (
        table.query.filter(table.ext_key == ext_key).first()
    )

    if existing_ess is None:
        """
        If ess doesnt exist, create new one
        https://marshmallow.readthedocs.io/en/stable/quickstart.html
        Add created_by, created_time autofileds
        """

        # auto fields created by and time
        payload['created_by'] = "REEEP"
        payload['created_time'] = datetime.datetime.utcnow().strftime(
            '%Y-%m-%d %H:%M:%S')

        schema = table_schema()
        new_ess = schema.load(payload)

        db.session.add(new_ess)
        db.session.commit()

        # Serialize and return the newly created ess in the response
        # data = schema.dump(new_ess)
        # print(data)
        print('new ess added')
        return new_ess.id
    else:
        """
        IF ess already exists, update existing ess
        TODO: detailed response message and mashmellow update format
        Add modified_by, modified_time autofileds
        """

        # auto fields update for modified by and time
        payload['modified_by'] = "REEEP"
        payload['modified_time'] = datetime.datetime.utcnow()

        updated_ess = (table.query.filter(
            table.ext_key == ext_key).update(payload))
        db.session.commit()
        print("{} updated in table {}".format(existing_ess.id, table.__name__))
        return existing_ess.id


def get_esp_id():
    """
    generate id from esp table look up
    Returns:
        [type]: [description]
    """
    return 3  # vitalite


null = None
full_payload = {
    "extKey": "ess_003",
    "customer": {
        "extKey": "CL2483772",
        "partyType": "Customer",
        "nameFirst": "John",
        "nameLast": "Customer1",
        "nameProvince": "Lusaka",
        "nameCity": "Shantumbu",
        "cdAreaCode": 260,
        "nameVillage": null,
        "textAddress": "asdf",
        "textPhoneNumber": "+123",
        "textEmail": null,
        "textGender": "M"
    },
    "beneficiary": null,
    "seller": {
        "extKey": "US038522",
        "partyType": "Seller",
        "nameFirst": "John",
        "nameLast": "Seller1",
        "nameProvince": null,
        "nameCity": null,
        "cdAreaCode": 260,
        "nameVillage": null,
        "textAddress": null,
        "textPhoneNumber": "+123",
        "textEmail": "seller1@supamoto.com",
        "textGender": null
    },
    "productId": "PT000233",
    # "acquisitionDate": 1602229140000,
    "acquisitionDate": '2020-03-05',
    "paymentType": "PAYG",
    "planDuration": 1106,
    "minimumPaymentPerMonth": 80.0,
    "downPayment": 150.0,
    "datePaidOff": null,
    "daysPaid": 30,
    "daysToPay": 1050,
    "currentDaysOutstanding": 0,
    "totalDaysOutstanding": 0,
    "totalFinancedAtTimeOfPurchase": 2950.0,
    "productUse": "Household",
    "productSubUse": null,
    "serialNumber": "76656644",
    "repossessionDate": null,
    "paygTransactions": [
        {
            "extKey": "PA107500957",
            "amtPayment": 150.0,
            "dtPayment": 1602079630000,
            "textPaymentStatus": "Active",
            "textTransactionType": "Mobile Money",
            "textSms": "Thank you!"
        }
    ],
    "events": null,
    # cannot be null, a foreign key constraint (`id_customer`) REFERENCES `party` (`id`))')
    "id_product": 2,
    "id_customer": 81547,
    "id_esp": get_esp_id()
}


# Quick way to add new record
# new_ess = ShsEss(**payload)
# db.session.add(new_ess)
# db.session.commit()

"""
Using SHS_ESS Wrapper
"""
# shs_post = ShsEssWrapper(payload, token)


"""
STEP 0 Map payload colunms to tables
"downPayment":"nbr_down_payment", dollar conversion  TODO: query API 
"update dateformat conversion"
"""
translation = {
    "acquisitionDate": "dt_acquisition",
    "datePaidOff": "dt_paid_off",
    "currentDaysOutstanding": "nbr_curr_days_outstanding",
    "daysPaid": "nbr_days_paid",
    "daysToPay": "nbr_days_to_pay",
    "minimumPaymentPerMonth": "nbr_min_monthly_payment",
    "planDuration": "nbr_plan_duration",
    "totalDaysOutstanding": "nbr_total_days_outstanding",
    "paymentType": "payment_type",
    "productUse": "text_product_use",
    "serialNumber": "text_serial_number",
    "productSubUse": "text_sub_product_use",
    "extKey": "ext_key",
    "repossessionDate": "dttm_repossession",
    "totalFinancedAtTimeOfPurchase": "amt_purchase_financed_zmw",
    "downPayment": "nbr_down_payment",
    # cannot be null, foreign key constraint (`id_product`) REFERENCES `product` (`id`))')
    "minimumPaymentPerMonth": "nbr_min_monthly_payment_zmw",
    # cannot be null, a foreign key constraint (`id_customer`) REFERENCES `party` (`id`))')
    "productId": "id_product",
}
payload = map_rekey(full_payload, translation)

"""
STEP 1
Look up combination of ID_ESP and main extKey from JSON in the SHS_ESS db table
return ess_shs_id from shs_ess table
seperate cutomer, seller and paygtransactions objects
"""
# my_dict.pop('key', None)
# payload.pop('customer', None)
# payload.pop('beneficiary', None)
# payload.pop('seller', None)
# payload.pop('paygTransactions', None)
# payload.pop('events', None)

id_shs_ess = update_insert_ess_shs(test_payload,ShsEss,ShsEssSchema,"ext_key")


"""
# STEP 2
# Look up paygtransaction extKey in PAYG db table
# if it exist, add id_shs_ess to payg_payload to reference user payment and insert or update
"""

# payg_payload = full_payload.get("paygTransactions")[0]
# payg_payload['id_shs_ess'] = id_shs_ess
# payg_payload['id_esp'] = get_esp_id()

# print(payg_payload)
# id_payg = update_insert_ess_shs(payg_payload,PayG,PayGSchema,"extKey")

# return payment id to be used further

# print(id_payg)

"""
[summary]
1ST SKETCH: Insert/update steps for SHS

# Pull ID_ESP from ESP table based on post token, and save for future use in processing the record
Look up combination of ID_ESP and main extKey from JSON in the SHS_ESS db table

if it is already there:
    update green fields from post
    update ID_ESP from token
    set warning if ID_ESP changes
    pull and save ID from SHS_ESS for future use
if it is NOT already there:
    insert green fields from post
    insert ID_ESP from token
    once db insert completes, re-look up based on ID_ESP and main extKey, and pull and save ID for future use

Look up paygtransaction extKey and ID_ESP in PAYG db table

if there, update and if not insert:
yellow fields in PAYG table, including both what is from post itself
ID_SHS_ESS and ID_ESP from values saved in previous steps
update EVENTS table, analogous to PAYG table, if not null

look up customer extKey and ID_ESP in PARTY table where PARTY_TYPE == 'Customer'
insert/update analogous to above
pull ID field from party table and retain for future use
look up seller extKey and ID_ESP in PARTY table, analagous to above, except PARTY_TYPE == 'Seller'


look up productId and ID_ESP against EXT_KEY and ID_ESP in PRODUCT table
if it is already there:
pull ID value and retain for inclusion in SHS_ESS table
if it is NOT already there:
insert a row setting EXT_KEY to productId and ID_TIER to 0
pull ID value and retain for inclusion in SHS_ESS table
Maybe send warning for unidentified product? (not error, just warning)


Update SHS_ESS table with values from other tables
Foreign keys to other tables, MUST do as part of load process
ID_PRODUCT > ID from PRODUCT table
ID_CUSTOMER > ID from PARTY table where PARTY_TYPE == 'Customer'
ID_SELLER > ID from PARTY table where PARTY_TYPE == 'Seller'
Status and latest value fields, may do as part of a nightly batch outside of load process
pull most recent PAYG record for each SHSS_ESS record
payment_date_current //most important
id_payg_current
payment_amount_current //in USD, needs forex, also, not important
text_current_payment_status //not important
text_transaction_type_current // also not important
Forex functions: ZMW to USD // not top priority
several fields in PAYG table (including at least one summarized in SHS_ESS table)
AMT_PURCHASE_FINANCED in SHS_ESS table

"""
