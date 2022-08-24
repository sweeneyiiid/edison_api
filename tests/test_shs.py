import unittest
import os
import base64
from app import application
from app.services.shs_ess_wrapper import ShsEssWrapper

"""
SHS test cases
Test cases for shs data
"""

DATA = [
    {
        "extKey": "string",
        "customer": {
        "extKey": "string",
        "partyType": "string",
        "nameFirst": "string",
        "nameLast": "string",
        "nameProvince": "string",
        "nameCity": "string",
        "cdAreaCode": "string",
        "nameVillage": "string",
        "textAddress": "string",
        "textPhoneNumber": "string",
        "textEmail": "string",
        "textGender": "string"
        },
        "beneficiary": "string",
        "microgrid": {
        "extKey": "string",
        "nameProvince": "string",
        "nameCity": "string",
        "nameVillage": "string",
        "textCoordinates": "string",
        "managers": "string",
        "dtInstallation": "string",
        "nbrAvgSolarInsolationAnnual": "string",
        "nbrBaseLoadKw": "string",
        "nbrCapacityKw": "string",
        "nbrStorageKwh": "string",
        "microgridHourlys": "string",
        "partyOperations": "string"
        },
        "connectionDate": 1578873600000,
        "paymentStatus": "Active",
        "productUse": "Household",
        "subProductUse": "string",
        "appliances": "string",
        "events": "string",
        "whTransactions": {
        "extKey": "string",
        "dtStart": "string",
        "nbrDaysPurchased": 0,
        "nbrAmtPaidZmw": 0
        }
    }
]

TOKEN = os.getenv('TEST_TOKEN_SHS')

class TestSHSWrapper(unittest.TestCase):
    def setUp(self):
        self.shs_import = ShsEssWrapper(DATA,TOKEN)
        pass
    
    # test case  
    def test(self):
        self.assertTrue(True)

    # test method get data  
    def get_data(self):
        get_data = self.shs_import.get_data()
        valid = self.shs_import.response['status']
        print(valid)
        self.assertTrue(valid)
    
    # test validate method
    def get_esp_id(self):
        get_esp_id = self.shs_import.get_esp_id()
        self.assertEqual(get_esp_id, 'FOO')

        valid = self.shs_import.response['status']
        self.assertFalse(valid)

if __name__ == '__main__':
    unittest.main()
