import sys
import os
sys.path.append("..")

from core.Log import Log
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
                '$match': {
                    '$and': [{'Quote': reported_currency }, {'Year': calendar_year }]
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
                '$sort': {'Day': -1}
            }, 
            {
                '$limit': 1
            }
        ])
    
    
    def create_usd_financial_report_collections_version(self):
        self.drop_collection(self.collection_name_usd)
        
        log = Log(f"{self.domain}_to_usd")
        log.append(f"Domain: {self.domain}")
        log.append(f"Start: { get_string_timestamp() }")
                
        query_result = self.get_company_reports_data()
        report_skiped = 0
        counter = 1

        for result in query_result:
            reported_currency = result['reportedCurrency']
            calendar_year = result['calendarYear']
            
            # if calendar_year == get_year():
            if calendar_year == "2022":
                report_skiped = report_skiped + 1
                continue

            # For legacy FMP API financial report
            if "calendarYear" in result:
                result["calendarYear"] = result["date"].split('-')[0]

            if reported_currency == "USD":
                exchange_rate = {
                        'Pair':'USD',
                        'Date':result['date'],
                        'Price': 1
                    }
            else:
                fx_results = self.get_exchange_by_date_and_quote('fx_last_exrate', result)
                for fx in fx_results:
                    exchange_rate = {
                        'Pair':fx['Pair'],
                        'Date': fx['Date'],
                        'Price': fx['Price']
                    }


            for field in self.fields:
                result[field] = round(result[field] / exchange_rate['Price'], 2)
            
            result['exchange_rate'] = exchange_rate
            
            try:
                self.inset_values_into_usd_collection_version(result)
            except Exception as error:
                log.append(f"{error} in {result['_id']}")
                print(error)
            
            
            print(counter)
            counter = counter + 1

        log.append(f"Insert records finished")
        index_result = self.create_indexes("usd")
        log.append(f"Index created in: {self.domain}, {index_result}")
        log.append(f"Total records: {counter + report_skiped}")
        log.append(f"Total records inserted: {counter}")
        log.append(f"Report Skiped cause calendarYear: {report_skiped}")
        log.append(f"End: {get_string_timestamp()}")
        log.append("* * * *\n\n")


    def drop_collection(self, coll_name):
        self.db[coll_name].drop()
    
    
    def create_indexes(self, collection_currency):
        if collection_currency == "usd":
            self.collection = self.db[self.collection_name_usd]
        else:
            self.collection = self.db[self.collection_name]
        
        
        if self.indexes is None:
            return None

        for index in self.indexes:
            for index_params in index.values():
                try:
                    create_index = f'self.collection.create_index({index_params})'
                    print(create_index)
                    exec(create_index)
                except Exception as error:
                    print(f"Error en creacion de indice {self.domain}")
                    print(error)
        
        return self.collection.index_information()


   

    

