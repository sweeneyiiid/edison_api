import os
import datetime
from datetime import date, timedelta

"""
Aggregate by start and end date
STEPS
Get collection by company name
Add new ts ISO field by adding days from 1970 https://medium.com/idomongodb/mongodb-unix-timestamp-to-isodate-67741ab32078
Limit the result to specific fields https://stackoverflow.com/questions/30996728/adding-subtracting-days-to-isodate-in-mongodb-shell
Count records in the list: suing pymongo specific abstractions https://stackoverflow.com/questions/37474784/query-datetime-with-pymongo
"""

pipeline  = [
    # add new field from timestamp
    {
        "$addFields": {
            'ts': {
                "$add": [datetime.datetime.utcfromtimestamp(0), { "$multiply": ["$time_stamp", 1000] }]
            }
        }
    },
    # filter by the last 34 days
    {
        "$match": {
            'ts': {
                "$gte": datetime.datetime.now() - timedelta(days=221),
                "$lt": datetime.datetime.now()
            }
        }
    },
    # count how many records
    { "$count": "count" }
]