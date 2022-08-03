import sys

from config.exec_order import incomeStatement, balanceSheet, cashFlow, outlook, profile
from noSql.mongo_operations import create_collection


# create_collection(profile['kwargs'])
# create_collection(incomeStatement['kwargs'])
# create_collection(balanceSheet['kwargs'])
create_collection(cashFlow['kwargs'])
# create_collection(outlook['kwargs'])

