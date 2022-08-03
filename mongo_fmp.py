import sys

from config.exec_order import incomeStatement
from noSql.create_mongo_collections import create_collection


create_collection(incomeStatement['kwargs'])

