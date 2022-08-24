from app import client
from flask import jsonify
from multiprocessing import Pool
import time
import dateparser
import requests


from app.utils.core import map_rekey, rename_keys
from app import db, ma
import datetime

# data models
from app.models.shs_ess.shs_ess_model import ShsEss, ShsEssSchema
from app.models.shs_ess.payg_model import PayG, PayGSchema
from app.models.shs_ess.product_model import Product, ProductSchema
from app.models.shs_ess.party_model import Party, PartySchema

from app.models.esp_model import Esp

class ShsEssWrapper():
    """
    Class SHS POST Service to Prod

    STEP 1: ESP: (Foreign Key Lookup)

    STEP 2: PRODUCT: (Foreign Key Lookup)
        look up productId and ID_ESP against EXT_KEY and ID_ESP in PRODUCT table
        if it is already there:
        pull ID value and retain for inclusion in SHS_ESS table
        if it is NOT already there:
        insert a row setting EXT_KEY to productId and ID_TIER to 0
        pull ID value and retain for inclusion in SHS_ESS table

        TODO: IF Doest exist, add dummy data 

    STEP 3: CUSTOMER: (Foreign Key Lookup)

    STEP 4: ESS Table GREEN
        Look up combination of ID_ESP and main extKey from JSON in the SHS_ESS db table
        return ess_shs_id from shs_ess table
        seperate cutomer, seller and paygtransactions objects

    STEP 5: YELLOW
        Look up paygtransaction extKey in PAYG db table
        If it exist, add id_shs_ess to payg_payload to reference user payment and insert or update

    STEP 6: BLUE and RED
        look up customer extKey and ID_ESP in PARTY table where PARTY_TYPE == 'Customer'
        insert/update analogous to above
        pull ID field from party table and retain for future use
        look up seller extKey and ID_ESP in PARTY table, analagous to above, except PARTY_TYPE == 'Seller'

    STEP 7: Back to SHS Table
        Update SHS_ESS table with values from other tables
        Foreign keys to other tables, MUST do as part of load process
        ID_PRODUCT > ID from PRODUCT table
        ID_CUSTOMER > ID from PARTY table where PARTY_TYPE == 'Customer'
        ID_SELLER > ID from PARTY table where PARTY_TYPE == 'Seller'
        Status and latest value fields, may do as part of a nightly batch outside of load process
        pull most recent PAYG record for each SHSS_ESS record
    return error if any

    test_key_dev: 2ee14bc2-3997-47d3-aad8-2d5aa26aa059
    Sample Post

        {
        "extKey": "AC2486003",
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
        "acquisitionDate": 1602229140000,
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
                "textSms": "Thank you! We have received your payment of 150 for account 76656644. Your next payment is due on 8 Nov 2020. "
            }
        ],
        "events": null
    }

    TODO: Date format fix (2020-12-03T09:52:27Z)

    """

    def __init__(self, data, token):
        self.data = data        
        self.response = {}
        self.token = token
        # define map rekey separately

    def get_data(self):
        """
        Get all the data sent through the post endpoing
        perfom extra functions or checks in this layer
        """
        response = {
            "status": True,
            'message': "valid"
        }
        self.response = response
        return self.data

    def get_esp_id(self):
        """
        Get the esp id from the POST 
        """
        esp_name = None
        esp_id = None
        try:
            esp_query = Esp.query.filter_by(text_api_token=self.token).first()
            esp_name = esp_query.name_company
            esp_id = esp_query.id
            response = {
            "status": True,
            'message': "valid"
            }
        except:
            response = {
                "status": True,
                'message': "esp token for this post is not valid"
            }
        self.response = response
        return esp_id

    def get_product_id(self, product_ext):
        """
        Get product id from the foreign key table product or add a new one with dummy data
        """
        product_id = None
        try:
            prod_query = Product.query.filter_by(ext_key=product_ext).first()
            product_id = prod_query.id
            response = {
            "status": True,
            'message': "valid"
            }
        except:
            # TODO:Create dummy product id
            response = {
                "status": False,
                'message': "Product id for this post is not valid"
            }
        self.response = response
        return product_id
    
    def get_customer(self, payload):
        """
        Get customer id from the foreign key table customer 
        """
        customer_id = None
        customer_ext = payload['extKey']

        # map data
        translation = {
                    "extKey":"ext_key",
                    "partyType":"party_type",
                    "nameFirst":"name_first",
                    "nameLast":"name_last",
                    "nameProvince":"name_province",
                    "nameCity":"name_city",
                    "cdAreaCode":"cd_area_code",
                    "nameVillage":"name_village",
                    "textAddress":"text_address",
                    "textPhoneNumber":"text_phone_number",
                    "textEmail":"text_email",
                    "textGender":"text_gender",
                }
        customer_payload = map_rekey(payload,translation)

        try:
            customer_query = Party.query.filter_by(ext_key=customer_ext).first()
            if customer_query is None:

                # add new customer
                customer_payload['created_by'] = "REEEP"
                customer_payload['created_time'] = datetime.datetime.utcnow().strftime(
                '%Y-%m-%d %H:%M:%S')
                
                schema = PartySchema()
                new_ess = schema.load(customer_payload)

                db.session.add(new_ess)
                db.session.commit()
                customer_id = new_ess.id

            else:
                
                # update customer

                # customer_payload['modified_by'] = "REEEP"
                # customer_payload['modified_time'] = datetime.datetime.utcnow()
                # customer_query_update = Party.query.filter_by(ext_key=customer_ext).update(customer_payload)
                # db.session.commit()
                # ess_id = ess_query.id
                # print("ess updated")

                customer_id = customer_query.id
            response = {
            "status": True,
            'message': "valid"
            }
        except:
            response = {
                "status": False,
                'message': "Product id for this post is not valid"
            }
        self.response = response
        return customer_id

    def get_ess(self, payload):
        """
        Get ess id from table shs_ess or update if it already exists
        Clean data
        TODO: Fix date format issue
        """
        # map data   
        translation = {
            "acquisitionDate":"dt_acquisition",
            "datePaidOff":"dt_paid_off",
            "currentDaysOutstanding":"nbr_curr_days_outstanding",
            "daysPaid":"nbr_days_paid",
            "daysToPay":"nbr_days_to_pay",
            "minimumPaymentPerMonth":"nbr_min_monthly_payment",
            "planDuration":"nbr_plan_duration",
            "totalDaysOutstanding":"nbr_total_days_outstanding",
            "paymentType":"payment_type",
            "productUse": "text_product_use",
            "serialNumber":"text_serial_number",
            "productSubUse":"text_sub_product_use",
            "extKey":"ext_key",
            "repossessionDate":"dttm_repossession",
            "totalFinancedAtTimeOfPurchase":"amt_purchase_financed_zmw",
            "downPayment":"nbr_down_payment",
            "minimumPaymentPerMonth":"nbr_min_monthly_payment_zmw", # cannot be null, foreign key constraint (`id_product`) REFERENCES `product` (`id`))')
            "productId":"id_product", # cannot be null, a foreign key constraint (`id_customer`) REFERENCES `party` (`id`))')
        }
        ess_payload = map_rekey(payload,translation)

        # date conversion
        date_time = dateparser.parse(str(ess_payload['dt_acquisition']))
        ess_payload['dt_acquisition'] = date_time.strftime('%Y-%m-%d')

        # pop nested dict records
        ess_payload.pop('customer', None)
        ess_payload.pop('beneficiary', None)
        ess_payload.pop('seller', None)
        ess_payload.pop('paygTransactions', None)
        ess_payload.pop('events', None)

        ess_id = None
        ess_ext = payload['extKey']
        
        try:
            ess_query = ShsEss.query.filter_by(ext_key=ess_ext).first()
            if ess_query is None:
                # add new ess
                ess_payload['created_by'] = "REEEP"
                ess_payload['created_time'] = datetime.datetime.utcnow().strftime(
                '%Y-%m-%d %H:%M:%S')
                
                schema = ShsEssSchema()
                new_ess = schema.load(ess_payload)

                db.session.add(new_ess)
                db.session.commit()
                print("ess added")
                ess_id = new_ess.id

                # pass
            else:
                # update ess
                # auto fields update for modified by and time
                ess_payload['modified_by'] = "REEEP"
                ess_payload['modified_time'] = datetime.datetime.utcnow()
                ess_query_update = ShsEss.query.filter_by(ext_key=ess_ext).update(ess_payload)
                db.session.commit()
                ess_id = ess_query.id
                print("ess updated")

            response = {
            "status": True,
            'message': "valid"
            }
        except:
            response = {
                "status": False,
                'message': "ESS id for this post is not valid"
            }
        self.response = response
        return ess_id

    def update_payg(self, payload, id_shs_ess, id_esp):
        """
        Insert new unique payg record 
        Look up paygtransaction extKey and ID_ESP in PAYG db table
        if there, update and if not insert
        TODO: Update date format and include payment_amount_zmw
        """

        # map data   
        translation = {
            "amtPayment":"payment_amount",
            "dtPayment":"payment_date",
            "textPaymentStatus":"text_payment_status",
            "textTransactionType":"text_transaction_type",
            "textSms":"text_sms",
            "extKey":"ext_key",
        }
        payg_payload = map_rekey(payload[0],translation)

        # date conversion
        date_time = dateparser.parse(str(payg_payload['payment_date']))
        payg_payload['payment_date'] = date_time.strftime('%Y-%m-%d')

        # add shs_ess_id
        payg_payload["id_shs_ess"] = id_shs_ess
        payg_payload["id_esp"] = id_esp
        payg_payload["payment_amount_zmw"] = 100 #TODO: need to inlcude payment amount zmw

        payg_id = None
        payg_ext = payg_payload["ext_key"]
        ess_ext = id_shs_ess
        ess_esp = id_esp

        try:
            payg_query = PayG.query.filter_by(ext_key=payg_ext, id_esp=ess_esp).first()

            if payg_query is None:

                # add new payg record
                payg_payload['created_by'] = "REEEP"
                payg_payload['created_time'] = datetime.datetime.utcnow().strftime(
                '%Y-%m-%d %H:%M:%S')
                
                schema = PayGSchema()
                new_ess = schema.load(payg_payload)

                db.session.add(new_ess)
                db.session.commit()
                print("payg added")
                payg_id = new_ess.id

                # pass
            else:
                # update ess
                # auto fields update for modified by and time
                payg_payload['modified_by'] = "REEEP"
                payg_payload['modified_time'] = datetime.datetime.utcnow()
                payg_query_update = PayG.query.filter_by(ext_key=payg_ext, id_esp=ess_esp).update(payg_payload)
                db.session.commit()
                payg_id = payg_query.id
                print("payg updated")

            response = {
            "status": True,
            'message': "valid"
            }
        except:
            response = {
                "status": False,
                'message': "payg id for this post is not valid"
            }
        self.response = response
        return payg_id

    def get_forex_conversion(self, zmw):
        """[convert zmw to dollar or other currencies]
        Args:
            zmw ([type]): [the currency value to convert from]

            https://exchangeratesapi.io/
        """

        # Where USD is the base currency you want to use
        url = 'https://v6.exchangerate-api.com/v6/YOUR-API-KEY/latest/USD'

        # Making our request
        response = requests.get(url)
        data = response.json()
        pass

    def ess_data_flow(self, payload):
        """
        ESS data Flow 
        STEPS:
        Get ESP and update payload
        Get Product_id and update payload
        Get Customer_id and update payload
        Get SHS_ESS_id and pass to payg
        TODO: Get Payg id, get forex value and pass back to shs_ess table
        """

        # esp
        
        esp_id = self.get_esp_id()
        payload['id_esp'] = esp_id

        # product
        product_id = self.get_product_id(payload["productId"])
        payload['id_product'] = product_id

        # customer
        # if(self.response['status']):
        customer_id = self.get_customer(payload["customer"])
        payload['id_customer'] = customer_id

        # ess
        ess_id = self.get_ess(payload)

        # payg

        payg_record = self.update_payg(payload["paygTransactions"], ess_id, esp_id)

        # forex call and back to ess_table
        # update shs_ess table with ID_PRODUCT, ID_CUSTOMER, ID_SELLER, id_payg, forex and other records from payg

        return ess_id

    def save_to_sql(self):
        """
        Save data to SQL Tables
        STEPS
        get api data
        """
        
        api_data = self.get_data()

        """
        Check that response is true
        For each response data, 
        insert into the appropriate ESP database
        TODO: update respoonse message for each insert, with error message pointing to unique entry for easy tracking
        """
        if(self.response['status']):
            try:
                index = 0
                for item in api_data:
                    ess_data_flow = self.ess_data_flow(item)

                    print(self.response)


                    # id_ess = self.get_ess_id(ess_data)

                    # item['time_stamp'] = time.time() 
                    # database[esp_name].insert_one(item) 
                    # self.response['esp'] = esp_name

                    self.response['message'] = "data saved succesfully"
                    index += 1
                    self.response['entries'] = index
                return {'message': 'data saved'}, 200
            except:
                return {'message': 'data not saved', 'reason': self.response['message']}, 401 # return detailes error, and possibly email notification

    def email_notification(self):
        """
        Decide if we need email notification
        """
        pass

    def output(self):
        """
        Return the class output from save to mongo and any other functionalities
        """
        save_to_sql = self.save_to_sql()

        response_object = {
            'message': self.response,
        }
        return response_object, 200
