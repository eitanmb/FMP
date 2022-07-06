import os
import sys
sys.path.append("..")

from distutils.log import error
from helpers.utilities import get_date, get_subdirectories_by_date, print_messages
from core.FmpAPI import FmpAPI, FmpTickers
from config.dir_structure import *
from config.endpoints import ENDPOINTS


BASE_DIR: str = os.path.dirname(os.path.abspath('fmp'))

DIRS: object = {
    'ROOT_JSON_DIR': "",
    'CURRENT_JSON_FOLDER': ""
}

DIRS['ROOT_JSON_DIR'] = f'{ BASE_DIR }/json'

subdirectories_list: list = []
date: str = get_date()
subdirectories_list = get_subdirectories_by_date(date)
DBNAME = f'FMP_{ subdirectories_list[0] }_{ subdirectories_list[1] }'

create_json_directory_structure(DIRS["ROOT_JSON_DIR"], subdirectories_list)

if DIRS['CURRENT_JSON_FOLDER'] == "":
    DIRS['CURRENT_JSON_FOLDER'] = set_current_json_folder(
        DIRS['ROOT_JSON_DIR'], subdirectories_list)


TICKERS_PATH: object = {
    'tickers_financial_info': f'{ DIRS["CURRENT_JSON_FOLDER"] }/tickers_financial_info.json',
    'tradeble_tickers': f'{ DIRS["CURRENT_JSON_FOLDER"] }/tradeble_tickers.json',
    'symbols': f'{ DIRS["CURRENT_JSON_FOLDER"] }/symbols.json',
    'forex_pairs': f'{ DIRS["CURRENT_JSON_FOLDER"] }/forex_pairs.json'

}

def isFile(file):
    return os.path.exists(file)


def create_tickers_file(file_info):
    try:
        FmpTickers.create_tickers_list(
            file_info['dir'], file_info['endpoint'], file_info['file_name'])
        print_messages(file_info['file_name'], "created")
    except Exception as error:
        print_messages(error)


tickers_file: object = {
    "financial": {
        "dir": DIRS['CURRENT_JSON_FOLDER'],
        "endpoint": ENDPOINTS['financial_list'],
        "file_name": 'tickers_financial_info.json'
    },
    "tradeble": {
        "dir": DIRS['CURRENT_JSON_FOLDER'],
        "endpoint": ENDPOINTS['tradeble_list'],
        "file_name": 'tradeble_tickers.json'
    },
    "stock": {
        "dir": DIRS['CURRENT_JSON_FOLDER'],
        "endpoint": ENDPOINTS['stock_list'],
        "file_name": 'symbols.json'
    },
    "forex": {
        "dir": DIRS['CURRENT_JSON_FOLDER'],
        "endpoint":  ENDPOINTS['forex_pairs'],
        "file_name": 'forex_pairs.json'
    }
}

if not isFile(TICKERS_PATH['tickers_financial_info']):
    create_tickers_file(tickers_file['financial'])

if not isFile(TICKERS_PATH['tradeble_tickers']):
    create_tickers_file(tickers_file['tradeble'])

if not isFile(TICKERS_PATH['symbols']):
    create_tickers_file(tickers_file['stock'])

if not isFile(TICKERS_PATH['forex_pairs']):
    create_tickers_file(tickers_file['forex'])
