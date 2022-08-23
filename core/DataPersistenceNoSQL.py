import sys
import os
sys.path.append("..")

from dotenv import load_dotenv
from helpers.utilities import *
import json
from pymongo import MongoClient

load_dotenv()
MONGO_DB_CNN = os.environ.get("MONGO_DB_CONN")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")

class NoSqlDataPersistence:
    
    def __init__(self, **kwargs):
        self.collection_name = kwargs['noSql']['collection_name']
        self.collection_name_usd = kwargs['noSql']['collection_name_usd']
        self.db = self.get_database()
        self.domain = kwargs['domain']
        self.fields = kwargs['noSql']['fields']
        self.folder = kwargs['folder']
        self.indexes = kwargs['noSql']['indexes'],
        
    
    def get_database(self):
        client = MongoClient(MONGO_DB_CNN)
        return client[MONGO_DB_NAME]


class NoSqlOperations(NoSqlDataPersistence):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    
    def insert_collection_data_from_json_files(self):
        counter = 1
        self.collection = self.db[self.collection_name]

        for filename in os.listdir(self.folder):
            f = os.path.join(self.folder, filename)

            if os.path.isfile(f):
                collection_data = open(f)

            try:
                doc = json.load(collection_data)
                
                if len(doc) > 0:
                    print(counter)
                    if self.domain == "outlook":
                        print(self.collection.insert_one(doc))
                    elif self.domain == "forex":
                        print(self.collection.insert_many(doc))
                    else:    
                        print(self.collection.insert_one(doc[0]))

            except Exception as e:
                print(e)

            counter = counter + 1
        
        self.create_indexes(self.collection_name)

    
    def inset_values_into_usd_collection_version(self, data):
        self.collection = self.db[self.collection_name_usd]
        return self.collection.insert_one(data)
    
    
    def get_company_reports_data(self):
        self.collection = self.db[self.collection_name]
        return self.collection.find()

    
    def get_exchange_by_date_and_quote(self, coll_name, result):
        reported_currency = result['reportedCurrency']
        calendar_year = result['calendarYear']

        return self.db[coll_name].aggregate([
            {
                '$project': {
                    'Pair': 1, 
                    'Date': 1, 
                    'formatedDate': {'$toDate': '$Date'}, 
                    'Price': {
                        '$replaceOne': {'input': '$Price', 'find': ',', 'replacement': ''}
                    }
                }
            }, 
            {
                '$addFields': {
                    'Quote': {'$substrCP': ['$Pair', 3, {'$strLenCP': '$Pair'}]}, 
                    'Price': {'$toDouble': '$Price'}, 
                    'Year': {'$year': '$formatedDate'}, 
                    'Month': {'$month': '$formatedDate'}, 
                    'Day': {'$dayOfMonth': '$formatedDate'}
                }
            }, 
            {
                '$addFields': {
                    'Year': {'$toString': '$Year'}
                }
            }, 
            {
                '$match': {
                    '$and': [ {'Month': 12}, {"Quote":reported_currency}, {"Year":calendar_year} ]
                }
            }, 
            {
                '$project': {
                    'Pair': 1, 
                    'Quote': 1, 
                    'Date': 1, 
                    'Price': 1
                }
            }, 
            {
                '$limit': 1
            }
        ])
    
    
    def create_usd_financial_report_collections_version(self):
        query_result = self.get_company_reports_data()

        for result in query_result:
            reported_currency = result['reportedCurrency']
            calendar_year = result['calendarYear']

            # print(calendar_year)
            if calendar_year == get_year():
                continue

            # For legacy FMP API financial report
            if "calendarYear" in result:
                result["calendarYear"] = result["date"].split('-')[0]

            # print(reported_currency)
            if reported_currency == "USD":
                exchange_rate = {
                        'Pair':'USD',
                        'Date':result['date'],
                        'Price': 1
                    }
            else:
                fx_results = self.get_exchange_by_date_and_quote('forex', result)
                for fx in fx_results:
                    exchange_rate = {
                        'Pair':fx['Pair'],
                        'Date': fx['Date'],
                        'Price': fx['Price']
                    }

            # print(exchange_rate)
            for field in self.fields:
                result[field] = round(result[field] / exchange_rate['Price'], 2)
                # print(field, ": ", result[field])
            
            result['exchange_rate'] = exchange_rate
            print(result)
            print(self.inset_values_into_usd_collection_version(result))

        self.create_indexes(self.collection_name_usd)
    
    
    def drop_collection(self, coll_name):
        self.db[coll_name].drop()
    
    
    def create_indexes(self, coll_name):
        if self.indexes[0] is None:
            return

        for index in self.indexes:
            for index_params in index.values():
                try:
                    exec(f'{self.db[coll_name]}.create_index({index_params})')
                except Exception as error:
                    print(error)
                finally:
                    print(self.db[coll_name].index_information())


   

    

