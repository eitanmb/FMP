from dataclasses import fields
import sys
import os
sys.path.append("..")

from dotenv import load_dotenv
from helpers.utilities import *
import json
from pymongo import MongoClient

load_dotenv()
MONGO_DB = os.environ.get("MONGO_DB_CONN")


class NoSqlDataPersistence():
    
    def __init__(self, **kwargs):
        self.folder = kwargs['folder']
        self.collection_name = kwargs['noSql']['collection_name']
        self.indexes = kwargs['noSql']['indexes'],
        self.domain = kwargs['domain']
        self.db = self.get_database()
        self.collection = self.db[self.collection_name]

    def get_database(self):
        client = MongoClient(MONGO_DB)
        return client['ptraDB']
    

    def insert_collection_data_from_json_files(self):
        counter = 1

        for filename in os.listdir(self.folder):
            f = os.path.join(self.folder, filename)

            if os.path.isfile(f):
                company_data = open(f)

            try:
                doc = json.load(company_data)
                if len(doc) > 0:
                    print(counter)
                    if self.domain == "outlook":
                        print(self.collection.insert_one(doc))
                    else:
                        print(self.collection.insert_one(doc[0]))

            except Exception as e:
                print(e)

            counter = counter + 1


    def create_collection(self):
        self.collection = self.db[self.collection_name]
        self.collection.drop()
        print(f'current folder: {self.folder}')

    
    def create_indexes(self):

        if self.indexes is None:
            return
       
        for index in self.indexes:
            for query in index.values():
                try:
                    exec(query)
                except Exception as error:
                    print(error)
                finally:
                    print(self.collection.index_information())
