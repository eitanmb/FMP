# Requires the PyMongo package.
# https://api.mongodb.com/python/current
from pymongo import *
import pprint
import json
import re

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')
filter={
    'financialsAnnual.income': {
        '$elemMatch': {
            'date': {
                '$in': [
                    re.compile(r"2011"), re.compile(r"2010"), re.compile(r"2009")
                ]
            },
            'revenue': {
                '$gt': 0
            },
            'costOfRevenue': {
                '$gt': 0
            },
            'researchAndDevelopmentExpenses': {
                '$eq': 0
            }
        }
    }
}

result = client['dbfmp']['outlook'].find(
  filter=filter
)



# /**
#  * field: The field name
#  * expression: The expression.
#  */
# {
#   "financialsAnnual.income.expenses":
#    {
#           $map:
#                  {
#                    input: "$financialsAnnual.income",
#                    as: "income",
#                    in: { $subtract: [ "$$income.costAndExpenses", "$$income.costOfRevenue" ] }
#                  }
#             }
#
#
# }
