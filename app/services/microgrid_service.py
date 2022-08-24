from app import client
from app.models.esp_model import Esp
from flask import jsonify
import time

class MicroGridImport():
    """
    Class MicroGrid Service Steps
    Step1: Get Post data and token
    Step2: Get ESP name from post token
    Step3: Validate data
    Step4: Save to Mongo DB
    return error if any
    """
    def __init__(self, data, token):
        self.data = data        
        self.response = {}
        self.database = client.get_database('microgrid')
        self.token = token

    def get_data(self):
        """
        Get all the data sent through the post endpoing
        perfom extra functions or checks in this layer
        """
        response = {
            "status": "true",
            'message': "valid"
        }
        self.response = response
        return self.data

    def get_esp_name(self):
        """
        Get the esp name from the POST to use for collection creation
        TODO: check if esp is mg or shs
        db lookup to see if token matches esp, then get the curresponding esp name
        """
        esp_name = None
        try:
            esp_query = Esp.query.filter_by(text_api_token=self.token).first()
            esp_name = esp_query.name_company
            response = {
            "status": "true",
            'message': "valid"
            }
        except:
            response = {
                "status": "false",
                'message': "esp token for this post is not valid"
            }
        self.response = response
        return esp_name

    def validate_data(self):
        """
        Extra Validation if needed beyond the default model
        """
        response = {
            "status": "true",
            'message': "valid"
        }
        self.response = response
        pass
    
    def save_to_mongo(self):
        """
        Save data to mongo
        get api data
        get esp name
        save data to mongo db under esp collection
        add date stamp
        """
        api_data = self.get_data()
        esp_name = self.get_esp_name()
        database = self.database

        """
        Check that response is true
        For each response data, 
        add time stamp
        insert into the appropriate ESP database
        TODO: update respoonse message for each insert, with error message pointing to unique entry for easy tracking
        """
        if(self.response['status']):
            try:
                index = 0
                for item in api_data:
                    item['time_stamp'] = time.time() #object time stamp
                    database[esp_name].insert_one(item) 
                    self.response['message'] = "data saved succesfully"
                    self.response['esp'] = esp_name
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
        save_to_mongo = self.save_to_mongo()
        response_object = {
            'message': self.response,
        }
        return response_object, 200