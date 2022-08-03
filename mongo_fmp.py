import sys

from config.exec_order import incomeStatement, balanceSheet, cashFlow, outlook, profile
from core.DataPersistenceNoSQL import NoSqlDataPersistence


def create_data_persistence_noSQL(kargs):
    noSql = NoSqlDataPersistence(**kargs)
    noSql.create_data_persistence_noSQL()
    noSql.insert_collection_data_from_json_files()

create_data_persistence_noSQL(profile['kwargs'])
create_data_persistence_noSQL(incomeStatement['kwargs'])
create_data_persistence_noSQL(balanceSheet['kwargs'])
create_data_persistence_noSQL(cashFlow['kwargs'])
create_data_persistence_noSQL(outlook['kwargs'])





