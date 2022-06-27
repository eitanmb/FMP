import os
import sys

from helpers.utilities import *
from core.DataPersistence import SqlDataPersistence, drop_create_procedures
from core.DataDownload import DataDownload
from config.setup import DBNAME
from config.exec_order import exec_order
from sql.procedures import *
from sql.basics import *
from sql.definitions import CONNECTION

CONNECTION['database'] = DBNAME
create_db(CONNECTION)
engine = engine_connetion(CONNECTION)

downloading_data = ''

def get_data_download(kargs):
    download = DataDownload(**kargs)
    download.create_folder()
    download.fetch_data()


def get_data_persistence(kargs):
    sql = SqlDataPersistence(engine, **kargs)


def file_is_empty(file):
    if os.path.getsize(file) != 0:
        return False
    return True


def current_download_data():
    return get_lastTicker_info('lastTicker.txt')[0]


def halt():
    sys.exit()


def download_routine(data):
    global downloading_data
    print_messages("START:", data['current'])
    get_data_download(data['kwargs'])
    write_lastTicker_file('lastTicker.txt', data['next'], '0')
    downloading_data = current_download_data()
    print_messages("END:", data['current'])


def init():
    if current_download_data() == 'finished':
        print_messages('FINISHED')
        halt()

    if file_is_empty('lastTicker.txt'):
        downloading_data = 'profile'
    else:
        downloading_data = current_download_data()

    for data in exec_order:
        print(data['current'], downloading_data)
        if data['current'] == downloading_data:
            download_routine(data)

    drop_create_procedures(stp_getLastChangeOfYear, engine)
    drop_create_procedures(stp_to_exRate, engine)
    drop_create_procedures(stp_to_usd, engine)
