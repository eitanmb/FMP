import sys
sys.path.append("..")

from pymongo import *
import os
import json
from helpers.utilities import *
from .get_mongo_db import get_database

# _date = get_date()

def insert_collection_data_from_json_files(folder, collection):
    count = 1

    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        
        if os.path.isfile(f):
            company_data = open(f)

        try:
            doc = json.load(company_data)
            if len(doc) > 0:
                print(count)
                print(collection.insert_one(doc[0]))

        except Exception as e:
            print(e)

        count = count + 1

    # create_text_indexes( collection )


def create_collection(kwargs):
    db = get_database()
    collection_name = kwargs['noSql']['collection_name']
    collection = db[collection_name]
    folder = kwargs['folder']

    insert_collection_data_from_json_files(folder, collection)


# def create_text_indexes( collection_name ):
#     collection_text_indexes = collection_name.financialsAnnual.income.create_index({
#         date:"text",
#         calendarYear:"text",
#         symbol:"text"
#     })

