# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 10:52:20 2020

@author: dan
"""

from pymongo import MongoClient


pass_word = "r7hgth4PonRH5TQG"

# REEEP dev cluster
#connect_string = "mongodb+srv://admin:{pswd}@cluster0.ok5iq.mongodb.net/microgrid-ess?retryWrites=true&w=majority"

# Dans personal cluster
connect_string = "mongodb+srv://admin:{pswd}@cluster0.wzlug.mongodb.net/sample_airbnb?retryWrites=true&w=majority"

#database name
#db_name = "microgrid-ess"
db_name = "sample_airbnb"



#collection name
coll_in_name = "listingsAndReviews"
#coll_in_name = "Standard Microgrid"

key_field = "listing_url"

client = MongoClient(connect_string.format(pswd = pass_word))



db = client[db_name]

print(db.list_collection_names())





pipeline = [
    {
        '$limit': 10
    },
    {
        '$group': {
            '_id': {"dummy": "$availability.availability_30"},
            'count': {'$sum': 1}
        }
    }

]


print(list(db[coll_in_name].aggregate(pipeline)))






pipeline = [
    {
        '$limit': 100
    },
    {
        '$project': {
            key_field: 1,
            'new_field': {'$concat': ["$"+key_field, "_x"]}
        }
    },
    {
        '$out': "movies_scratch"
    }
]



print(list(db[coll_in_name].aggregate(pipeline)))

# NEXT: Re-load to same place and see what happens