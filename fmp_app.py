import sys

from helpers.utilities import *
from helpers.File import File
from core.DataPersistenceSQL import SqlDataPersistence, drop_create_procedure
from core.DataPersistenceNoSQL import NoSqlDataPersistence
from core.DataDownload import DataDownload
from config.setup import DBNAME
from config.exec_order import exec_order
from sql.procedures import *
from sql.basics import *
from sql.definitions import CONNECTION


CONNECTION['database'] = DBNAME
create_db(CONNECTION)
engine = engine_connetion(CONNECTION)


def get_data_download(kargs):
    download = DataDownload(**kargs)
    download.create_folder()
    download.fetch_data()


def create_data_persistence_sql(kargs):
    sql = SqlDataPersistence(engine, **kargs)
    sql.drop_table()
    sql.create_table()
    sql.add_indexes()
    sql.insert_data_from_dataframe()
    sql.alter_table()


def create_data_persistence_noSQL(kargs):
    noSql = NoSqlDataPersistence(**kargs)
    noSql.create_collection()
    noSql.insert_collection_data_from_json_files()
    noSql.create_indexes()



def current_download_data():
    return get_lastTicker_info('lastTicker.txt')[0]


def halt():
    sys.exit()


def download_routine(data):
    print_messages("START:", data['current'])
    get_data_download(data['kwargs'])
    write_lastTicker_file('lastTicker.txt', data['next'], '0')
    print_messages("END:", data['current'])


def drop_create_procedures():
    drop_create_procedure(stp_getLastChangeOfYear, engine)
    drop_create_procedure(stp_to_exRate, engine)
    drop_create_procedure(stp_to_usd, engine)


def init():
    current_download = ''

    if current_download_data() == 'finished':
        print_messages('FINISHED')
        halt()

    if File.file_is_empty('lastTicker.txt'):
        current_download = 'profile'
    else:
        current_download = current_download_data()

    for data in exec_order:
        print_messages(data['current'], ": expected to download ->", current_download)
        if data['current'] == current_download:
            download_routine(data)
            current_download = current_download_data()

    drop_create_procedures()

    for data in exec_order:
        print_messages("Sql executions on:", data['current'])
        if data['kwargs']['sql'] is not None:
            create_data_persistence_sql(data['kwargs'])

    
    for data in exec_order:
        print_messages("NoSql executions on:", data['current'])
        if data['kwargs']['noSql'] is not None:
             create_data_persistence_noSQL(data['kwargs'])

   
