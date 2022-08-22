import sys
import os
sys.path.append("..")

from dotenv import load_dotenv
from pymongo import MongoClient
from definitions import BS_FIELDS, CF_FIELDS, IS_FIELDS, IS_NOSQl, BS_NOSQl, CF_NOSQl
from helpers.utilities import get_year
load_dotenv()
MONGO_DB = os.environ.get("MONGO_DB_CONN")

client = MongoClient(MONGO_DB)
db = client['ptraDB']


def create_usd_financial_report_collections_version(db, coll_params, fields):
    query_result = get_company_reports_data(db, coll_params)

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
            fx_results = get_exchange_by_date_and_quote(db, 'fx_last_exrate', reported_currency, calendar_year)
            for fx in fx_results:
                exchange_rate = {
                    'Pair':fx['Pair'],
                    'Date': fx['Date'],
                    'Price': fx['Price']
                }

        # print(exchange_rate)
        for field in fields:
            result[field] = round(result[field] / exchange_rate['Price'], 2)
            # print(field, ": ", result[field])
        
        result['exchange_rate'] = exchange_rate
        print(result)
        print(inset_values_into_usd_collection_version(db, coll_params, result))


def inset_values_into_usd_collection_version(db, coll_params, data):
    coll_name = coll_params['collection_name']
    coll_name_usd = f"{coll_name}_USD"
    return db[coll_name_usd].insert_one(data)



def get_company_reports_data(db, coll_params):
    coll_name = coll_params['collection_name']
    return db[coll_name].find().limit(10)
    


def get_exchange_by_date_and_quote(db, coll_name, reported_currency, calendar_year):
   return db[coll_name].aggregate([

        {
            "$match": {
                "$and":[{"Quote":reported_currency}, {"Year":calendar_year}]
            }
        },
        {
            "$project": {
                "Pair":1,
                "Quote":1,
                "Date":1,
                "Price":{ "$toDouble":"$Price" }
            }
        },
        {
            "$sort": {"Day":-1}
        },
        {
            "$limit":1
        }
    ])


create_usd_financial_report_collections_version(db, IS_NOSQl, IS_FIELDS)
create_usd_financial_report_collections_version(db, BS_NOSQl, BS_FIELDS)
create_usd_financial_report_collections_version(db, CF_NOSQl, CF_FIELDS)