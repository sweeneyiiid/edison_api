from app import client
from app.models.esp_model import Esp
from flask import jsonify
import time
import json
from bson import json_util
from app.services.microgrid_ess_service import MicroGridESSImport
from bson.json_util import dumps, loads

import requests

"""
Pipelines 
"""
from app.pipelines.core import get_Hour_Minute, get_time_difference, get_wh_from_sockets
from app.pipelines import aggregate_by_date
from app.pipelines import key_replacement


DATABASE_NAME = 'microgrid-ess' 

class MicroGridESSExport(MicroGridESSImport):
    """
    Class to export microgrid ess service
    Step1: Inherit espname check from MicroGridESSImport
    https://stackoverflow.com/questions/10064688/cant-access-parent-member-variable-in-python
    https://stackoverflow.com/questions/45871797/python-inheritance-object-has-no-attribute-error
    Step2: pass parameters to class (token,db,pipeline,export_uri)
    """

    def __init__(self, token, params):
        self.token = token
        super(MicroGridESSExport, self).__init__(None, token)
        self._esp_name = self.get_esp_name()  # Inherit esp name and repond if error
        self.database =  client.get_database(DATABASE_NAME)
        self.params = params

    def get_database_data(self):
        """
        Check if no error in response
        Query mongo db and get information using the params passed
        Get DB
        Get Esp
        Get Collection name from params or use esp name
        Use Collection and pipeline to pull data from mongodb with parameters
        """
        if(self.response['status']):
            database = self.database
            esp_name = self._esp_name
            result = None
            try:
                collection = database[self.params['collection'] or esp_name] #use the provided collection of defualt to esp name
                default_pipeline = [ { "$match" : { "extKey" : { "$exists" : 1 } } }]
                result = list(collection.aggregate(self.params['pipeline'] or default_pipeline)) # run the params.pipeline or return default pipeline
                result[0] == True #check the data returned is not empty
                response = {
                "status": "true",
                'message': "collection and pipeline is valid"
                }
            except:
                response = {
                    "status": "false",
                    'message': "collection name or pipeline is invalid"
                }
            self.response = response
            return result

    def run_pipeline(self, collection, pipeline):
        """
        Run pipelines for each appended pipeline in the list
        """
        if(self.response['status']):
            database = self.database
            esp_name = self._esp_name
            result = None
            try:
                collection = database[collection or self.params['collection'] or esp_name] #use the provided collection of defualt to esp name
                default_pipeline = [ { "$match" : { "extKey" : { "$exists" : 1 } } }]
                result = list(collection.aggregate(pipeline or self.params['pipeline'] or default_pipeline)) # run the params.pipeline or return default pipeline
                result[0] == True #check the data returned is not empty
                response = {
                "status": "true",
                'message': "collection and pipeline is valid"
                }
            except:
                response = {
                    "status": "false",
                    'message': "collection name or pipeline is invalid"
                }
            self.response = response
            return result

    def get_wh_calculation(self, collection):
        """
        WH transaction conversion and update
        STEPS
        Get Time difference between sockets
        Calculate Start Stop Values
        Append result to project
        TODO: 
            Watt Hours per Day is required, 
            Payment Status is required, - 
            Transaction Type must be one of [Cash, Mobile Money, Token, Other] -
        """
        database = self.database
        collection = database[collection or self.params['collection']] #use the provided collection of defualt to esp name
        for r in collection.find(): # for each record in collection
            """
            STEPS
            Update or add  Add new field whSum into every whTransactions in the collection
            """
            for index, wh in enumerate(r['whTransactions']): # for each record in whTransactions
                wh_from_sockets = round(get_wh_from_sockets(wh),2)
                collection.update_one({"_id": r["_id"]}, {"$set": {
                    "whTransactions."+ str(index)+".whSum": wh_from_sockets,
                    "whTransactions."+ str(index)+".textTransactionType": "Mobile Money",
                    "whTransactions."+ str(index)+".textPaymentStatus": "Active",
                    "whTransactions."+ str(index)+".nbrWhPerDay": (wh_from_sockets/3),
                    "whTransactions."+ str(index)+".nbrWhAvg30": (wh_from_sockets/3),
                    }}, upsert=True) #use upsert to update document if it doestn exist
        print("wh processing done")
        pass

    def post_data_to_dev(self, collection, uri):
        """
        POST time specific data to appropriate endpoints
        http://ec2-18-156-5-118.eu-central-1.compute.amazonaws.com:8443/external-data/microgrid-ess/d5cbdb8b-68c9-4613-aeb8-793e3a8805bc
        STEPS
        GET data
        GET ESP
        GET post endpoint
        """
        database = self.database
        collection = database[collection or self.params['collection']] #use the provided collection or defualt to esp name
        records = collection.find()
        
        """
        URL construction
        """
        url =  (uri or "https://httpbin.org/anything/") + self.token #construct the url with token appended at the end
        # url =  ("https://httpbin.org/anything/") + self.token #construct the url with token appended at the end
        headers={"Content-Type":"application/json"}

        for r in records: # for each record in collection, post to the URLabove
            json_str = dumps([r])
            # print(json_str)
            rsp = requests.post(url, data=json_str, headers=headers, verify=False)
            print(str(rsp.text)) 
        
        return rsp

    def output(self):
        """
        Return the class output from get database pull
        """
        
        """
        Run pipelines
        Rekey
        WH Calculation
        """
        # coll_out_name = "rekey_test"

        # pipe1 = self.run_pipeline("actual",key_replacement.ess_pipeline)
        # pipe2 = self.get_wh_calculation(coll_out_name)

        get_esp_data = self.get_database_data()
        
        response_object = {
            'message': self.response,
            'data': get_esp_data
        }
        return response_object

