# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 10:52:20 2020

@author: dan
"""


# =============================================================================
# STEP 0: Basic setup and connect
# =============================================================================

from pymongo import MongoClient

#Mongo cluster connection password
pass_word = ""

# REEEP dev cluster
connect_string = "mongodb+srv://admin:{pswd}@cluster0.ok5iq.mongodb.net/microgrid-ess?retryWrites=true&w=majority"

#database names
db_name = "microgrid"
db_name_ess = "microgrid-ess"


#collection name (same for both DBs)
coll_in_name = "Standard Microgrid"

#key field (same for both DBs)
key_field = "extKey"

# Same connection for both DBs
client = MongoClient(connect_string.format(pswd = pass_word))


# =============================================================================
# STEP 1: Microgrid key replacement (use village)
# =============================================================================

db = client[db_name]

#print(db.list_collection_names())

mg_pipeline = [
    # {
    #     '$limit': 10
    # },
    {
        '$project': {
            "rawExtKey":"$extKey",
            key_field: {'$concat': ["$villageName", "_village"]},
            "averageAnnualSolarInsolation": 1,
            "baseLoadKw": 1,
            "capacityKw": 1,
            "cityName": 1,
            "coordinates": 1,
            "events": 1,
            "installationDate": 1,
            "managers": 1,
            "microgridHourlys": 1,
            "rco": 1,
            "rto": 1,
            "storageKwh": 1,
            "villageName": 1,
            "provinceName": 1
        }
    },
    {
        '$out': "mg_key_scratch"
    }
]

db = client[db_name]
db[coll_in_name].aggregate(mg_pipeline)


# =============================================================================
# STEP 2: ESS key replacement (use customer extKey)
# =============================================================================

ess_pipeline = [
    # {
    #     '$limit': 10
    # },
    {
        '$project': {
            "rawExtKey":"$extKey",
            key_field: {'$concat': ["$customer.extKey", "_customer"]},
            "customer":1,
            "beneficiary":1,
            "microgrid": {
                "rawExtKey": "$microgrid.extKey",
                key_field: {'$concat': ["$microgrid.nameVillage", "_village"]},
                "nameProvince":"$microgrid.nameProvince",
                "nameCity":"$microgrid.nameCity",
                "nameVillage":"$microgrid.nameVillage",
                "textCoordinates":"$microgrid.textCoordinates",
                "managers":"$microgrid.managers",
                "dtInstallation":"$microgrid.dtInstallation",
                "nbrAvgSolarInsolationAnnual":"$microgrid.nbrAvgSolarInsolationAnnual",
                "nbrBaseLoadKw":"$microgrid.nbrBaseLoadKw",
                "nbrCapacityKw":"$microgrid.nbrCapacityKw",
                "nbrStorageKwh":"$microgrid.nbrStorageKwh",
                "microgridHourlys":"$microgrid.microgridHourlys",
                "partyOperations":"$microgrid.partyOperations"
            },
            "connectionDate":1,
            "paymentStatus":1,
            "productUse":1,
            "subProductUse":1,
            "appliances":1,
            "whTransactions":1,
            "events":1


        }
    },
     {
        '$out': "mg_ess_key_scratch2"
    }   
]


db_ess = client[db_name_ess]
db_ess[coll_in_name].aggregate(ess_pipeline)


# =============================================================================
# STEP 3: Dump to JSON and post to INTG environment
# =============================================================================
