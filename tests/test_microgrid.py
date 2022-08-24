import unittest
import os
import base64
from app import application
from app.services.microgrid_service import MicroGridImport

"""
Pytest with  flask_restful: https://stackoverflow.com/questions/47042078/pytest-fails-to-import-module-installed-via-pip-and-containing-underscores/47099712#47099712
"""
"""
MicroGrid Import test cases
Quick Validation test for microgrid data with mock data and token
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

TOKEN = os.getenv('TEST_TOKEN')

class TestMicroGridImport(unittest.TestCase):
    def setUp(self):
        self.microgrid_import = MicroGridImport(DATA,TOKEN)
        pass
    
    # test case  
    def test(self):
        self.assertTrue(True)

    # test method get data  
    def get_data(self):
        get_data = self.microgrid_import.get_data()
        valid = self.microgrid_import.response['status']
        self.assertTrue(valid)
    
    # test validate method
    def get_esp_name(self):
        get_esp = self.microgrid_import.get_esp_name()
        print(get_esp)
        self.assertEqual(get_esp, 'FOO')

        valid = self.microgrid_import.response['status']
        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()
