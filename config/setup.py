import os
import sys
sys.path.append("..")

from helpers.utilities import get_date, get_subdirectories_by_date, print_messages
from core.FmpAPI import FmpTickers
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


TICKERS_FILES: object = {
    "financial": {
        "file_name": 'tickers_financial_info.json',
        "path_to_file": f"{DIRS['CURRENT_JSON_FOLDER']}/tickers_financial_info.json",
        "endpoint": ENDPOINTS['financial_list']
    },
    "tradeble": {
        "file_name": 'tradeble_tickers.json',
        "path_to_file": f"{DIRS['CURRENT_JSON_FOLDER']}/tradeble_tickers.json",
        "endpoint": ENDPOINTS['tradeble_list']
    },
    "stock": {
        "file_name": 'symbols.json',
        "path_to_file": f"{DIRS['CURRENT_JSON_FOLDER']}/symbols.json",
        "endpoint": ENDPOINTS['stock_list']
    },
    "forex": {
        "file_name": 'forex_pairs.json',
        "path_to_file": f"{DIRS['CURRENT_JSON_FOLDER']}/forex_pairs.json",
        "endpoint":  ENDPOINTS['forex_pairs']
    }
}

def isFile(ticker):
    file = ticker['path_to_file']
    return os.path.exists(file)


def create_tickers_file_if_not_exist(file_info):
    if not isFile(file_info):
        try:
            FmpTickers.create_tickers_list(file_info['path_to_file'], file_info['endpoint'])
            print_messages(file_info['file_name'], "created")
        except Exception as error:
            print_messages(error)


create_tickers_file_if_not_exist(TICKERS_FILES['financial'])
create_tickers_file_if_not_exist(TICKERS_FILES['tradeble'])
create_tickers_file_if_not_exist(TICKERS_FILES['stock'])
create_tickers_file_if_not_exist(TICKERS_FILES['forex'])
