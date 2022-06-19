from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_DB = os.environ.get("MONGO_DB_CONN")


def get_database():

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(MONGO_DB)

    # Create the database for our example (we will use the same database throughout the tutorial
    # return client['user_shopping_list']
    return client['ptraDB']
    
    