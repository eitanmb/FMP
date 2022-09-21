import os
import sys
sys.path.append("..")

from core.fmp.FmpAPI import FmpTickers
from config.fmp.fmp_endpoints import ENDPOINTS
from helpers.utilities import print_messages


def get_fmp_tickers_info(DIRS):
    TICKERS_FILES: object = {
        "financial":{
            "file_name": 'tickers_financial_info.json',
            "path_to_file": f"{DIRS['CURRENT_JSON_FOLDER']}/tickers_financial_info.json",
            "endpoint": ENDPOINTS['financial_list']
        },
        "tradeble":{
            "file_name": 'tradeble_tickers.json',
            "path_to_file": f"{DIRS['CURRENT_JSON_FOLDER']}/tradeble_tickers.json",
            "endpoint": ENDPOINTS['tradeble_list']
        },
        "stock":{
            "file_name": 'symbols.json',
            "path_to_file": f"{DIRS['CURRENT_JSON_FOLDER']}/symbols.json",
            "endpoint": ENDPOINTS['stock_list']
        },
        "forex":{
            "file_name": 'forex_pairs.json',
            "path_to_file": f"{DIRS['CURRENT_JSON_FOLDER']}/forex_pairs.json",
            "endpoint":  ENDPOINTS['forex_pairs']

        }
    }
    return TICKERS_FILES

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

def get_tickers(tickers):
    create_tickers_file_if_not_exist(tickers['financial'])
    create_tickers_file_if_not_exist(tickers['tradeble'])
    create_tickers_file_if_not_exist(tickers['stock'])
    create_tickers_file_if_not_exist(tickers['forex'])

def init(DIRS):
    TICKERS_FILES = get_fmp_tickers_info(DIRS)
    get_tickers(TICKERS_FILES)
    