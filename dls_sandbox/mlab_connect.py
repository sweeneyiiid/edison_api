# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 13:23:07 2020

@author: DanielSweeney
"""

from pymongo import MongoClient


pass_word = ""

# REEEP dev cluster
connect_string = "mongodb+srv://admin:{pswd}@cluster0.ok5iq.mongodb.net/microgrid-ess?retryWrites=true&w=majority"

# Dans personal cluster
#connect_string = "mongodb+srv://admin:{pswd}@cluster0.ok5iq.mongodb.net/microgrid-ess?retryWrites=true&w=majority"


client = MongoClient(connect_string.format(pswd = pass_word))



db = client["microgrid-ess"]

print(db.list_collection_names())



pipeline = [
    {
        '$group': {
            '_id': {"dummy": "$productUse"},
            'count': {'$sum': 1}
        }
    }
]



print(list(db["Standard Microgrid"].aggregate(pipeline)))


