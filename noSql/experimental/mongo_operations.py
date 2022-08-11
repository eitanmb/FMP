import sys
import os
sys.path.append("..")

from dotenv import load_dotenv
from helpers.utilities import *
import json
from pymongo import MongoClient

load_dotenv()
MONGO_DB = os.environ.get("MONGO_DB_CONN")


def get_database():
    client = MongoClient(MONGO_DB)
    return client['ptraDB']
    

def insert_collection_data_from_json_files(folder, collection, domain):
    counter = 1

    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)

        if os.path.isfile(f):
            company_data = open(f)

        try:
            doc = json.load(company_data)
            if len(doc) > 0:
                print(counter)
                if domain == "outlook":
                    print(collection.insert_one(doc))
                else:
                    print(collection.insert_one(doc[0]))

        except Exception as e:
            print(e)

        counter = counter + 1


def create_collection(kwargs):
    db = get_database()
    collection_name = kwargs['noSql']['collection_name']
    collection = db[collection_name]
    collection.drop()
    domain = kwargs['domain']
    folder = kwargs['folder']
    print(f'current folder: {folder}')

    insert_collection_data_from_json_files(folder, collection, domain)


# def create_text_indexes( collection_name ):
#     collection_text_indexes = collection_name.financialsAnnual.income.create_index({
#         date:"text",
#         calendarYear:"text",
#         symbol:"text"
#     })
