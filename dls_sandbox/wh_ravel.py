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
pass_word = "1llml8odsy4D5Px4"

# REEEP dev cluster
connect_string = "mongodb+srv://admin:{pswd}@cluster0.ok5iq.mongodb.net/microgrid-ess?retryWrites=true&w=majority"

#database name
db_name_ess = "microgrid-ess"


#collection name
coll_in_name = "Standard Microgrid"


# connect
client = MongoClient(connect_string.format(pswd = pass_word))


# =============================================================================
# STEP 1: put Wh data in tabular form
# =============================================================================

ess_pipeline = [
    {
        '$limit': 10
    },
    {
         '$project': {
                "essKey":"$extKey",
                "custKey": "$customer.extKey",
                "whTransactions":{"$arrayElemAt":["$whTransactions",0]}
             }
    },
    {
        '$project': {
                    "essKey":1,
                    "custKey":1,
                    'extKey':'$whTransactions.extKey',
                    'dtStart':'$whTransactions.dtStart',
                    'nbrDaysPurchased':'$whTransactions.nbrDaysPurchased',
                    'nbrAmtPaidZmw':'$whTransactions.nbrAmtPaidZmw',
                    'nbrCentaAmpLimit1':'$whTransactions.nbrCentaAmpLimit1',
                    'socket1Start0':'$whTransactions.socket1Start0',
                    'socket1Stop0':'$whTransactions.socket1Stop0',
                    'socket1Start1':'$whTransactions.socket1Start1',
                    'socket1Stop1':'$whTransactions.socket1Stop1',
                    'socket1Start2':'$whTransactions.socket1Start2',
                    'socket1Stop2':'$whTransactions.socket1Stop2',
                    'socket1Start3':'$whTransactions.socket1Start3',
                    'socket1Stop3':'$whTransactions.socket1Stop3',
                    'socket1Start4':'$whTransactions.socket1Start4',
                    'socket1Stop4':'$whTransactions.socket1Stop4',
                    'nbrCentaAmpLimit2':'$whTransactions.nbrCentaAmpLimit2',
                    'socket2Start0':'$whTransactions.socket2Start0',
                    'socket2Stop0':'$whTransactions.socket2Stop0',
                    'socket2Start1':'$whTransactions.socket2Start1',
                    'socket2Stop1':'$whTransactions.socket2Stop1',
                    'socket2Start2':'$whTransactions.socket2Start2',
                    'socket2Stop2':'$whTransactions.socket2Stop2',
                    'socket2Start3':'$whTransactions.socket2Start3',
                    'socket2Stop3':'$whTransactions.socket2Stop3',
                    'socket2Start4':'$whTransactions.socket2Start4',
                    'socket2Stop4':'$whTransactions.socket2Stop4',
                    'nbrCentaAmpLimit3':'$whTransactions.nbrCentaAmpLimit3',
                    'socket3Start0':'$whTransactions.socket3Start0',
                    'socket3Stop0':'$whTransactions.socket3Stop0',
                    'socket3Start1':'$whTransactions.socket3Start1',
                    'socket3Stop1':'$whTransactions.socket3Stop1',
                    'socket3Start2':'$whTransactions.socket3Start2',
                    'socket3Stop2':'$whTransactions.socket3Stop2',
                    'socket3Start3':'$whTransactions.socket3Start3',
                    'socket3Stop3':'$whTransactions.socket3Stop3',
                    'socket3Start4':'$whTransactions.socket3Start4',
                    'socket3Stop4':'$whTransactions.socket3Stop4',
                    'nbrCentaAmpLimit4':'$whTransactions.nbrCentaAmpLimit4',
                    'socket4Start0':'$whTransactions.socket4Start0',
                    'socket4Stop0':'$whTransactions.socket4Stop0',
                    'socket4Start1':'$whTransactions.socket4Start1',
                    'socket4Stop1':'$whTransactions.socket4Stop1',
                    'socket4Start2':'$whTransactions.socket4Start2',
                    'socket4Stop2':'$whTransactions.socket4Stop2',
                    'socket4Start3':'$whTransactions.socket4Start3',
                    'socket4Stop3':'$whTransactions.socket4Stop3',
                    'socket4Start4':'$whTransactions.socket4Start4',
                    'socket4Stop4':'$whTransactions.socket4Stop4',
                    'nbrCentaAmpLimit5':'$whTransactions.nbrCentaAmpLimit5',
                    'socket5Start0':'$whTransactions.socket5Start0',
                    'socket5Stop0':'$whTransactions.socket5Stop0',
                    'socket5Start1':'$whTransactions.socket5Start1',
                    'socket5Stop1':'$whTransactions.socket5Stop1',
                    'socket5Start2':'$whTransactions.socket5Start2',
                    'socket5Stop2':'$whTransactions.socket5Stop2',
                    'socket5Start3':'$whTransactions.socket5Start3',
                    'socket5Stop3':'$whTransactions.socket5Stop3',
                    'socket5Start4':'$whTransactions.socket5Start4',
                    'socket5Stop4':'$whTransactions.socket5Stop4',
                    'textPaymentStatus':'$whTransactions.textPaymentStatus'
        }
    },
    {
        '$out': "wh_ravel"
    }   
]


db_ess = client[db_name_ess]
print(list(db_ess[coll_in_name].aggregate(ess_pipeline)))


# =============================================================================
# STEP 3: Dump to JSON and post to INTG environment
# =============================================================================
