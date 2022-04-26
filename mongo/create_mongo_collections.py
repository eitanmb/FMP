import sys
sys.path.append("..")
from pymongo import *
import os
import json
from config.setup import DIRS
from helpers.utilities import *

from get_mongo_db import get_database


# Get the database
BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
folder: str      = f"/home/eitan/Programacion/FMP_2/json/2021/09/outlook"
dbname = get_database()
collection_name = dbname['outlook_2021_09']

print('folder: ', folder)


def create_collection_from_json( folder, collection ):

    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        
        # checking if it is a file
        if os.path.isfile(f):
            company_file = open(f)


        try:
            doc = json.load(company_file)
            if len(doc) > 0:
                print(collection.insert_one(doc))

        except Exception as e:
            print(e)


create_collection_from_json( folder, collection_name)