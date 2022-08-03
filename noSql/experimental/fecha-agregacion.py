# Requires the PyMongo package.
# https://api.mongodb.com/python/current
from pymongo import *
import pprint
import json


client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')
result = client['dbfmp']['outlook'].aggregate([
    {
        '$addFields': {
            'convertedDates': {
                '$map': {
                    'input': '$financialsAnnual.income',
                    'as': 'income',
                    'in': {
                        '$toDate': '$$income.date'
                    }
                }
            }
        }
    },
    {
        '$addFields': {
            'year': {
                '$map': {
                    'input': '$convertedDates',
                    'as': 'cYear',
                    'in': {
                        '$year': '$$cYear'
                    }
                }
            }
        }
    },
    {
        '$match': {
            'year': {
                '$all': [
                    2020, 2019, 2018
                ]
            }
        }
    },
    {
        '$match': {
            'financialsAnnual.income': {
                '$elemMatch': {
                    'revenue': {
                        '$gt': 0
                    },
                    'costOfRevenue': {
                        '$gt': 0
                    }
                }
            }
        }
    },
    {
        '$project': {
            'profile.symbol': 1,
            '_id': 0
        }
    }
])


for r in result:
    pprint.pprint(r)
