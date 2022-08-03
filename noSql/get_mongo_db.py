from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_DB = os.environ.get("MONGO_DB_CONN")


def get_database():
    client = MongoClient(MONGO_DB)
    return client['ptraDB']
    
    