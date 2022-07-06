from helpers.utilities import get_date, get_subdirectories_by_date
from core.FmpAPI import FmpAPI, FmpTickers
from config.dir_structure import *
from config.endpoints import ENDPOINTS
import os
import sys
sys.path.append("..")


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

if not os.path.exists(TICKERS_PATH['tickers_financial_info']):
    try:
        FmpTickers.create_tickers_list(
            DIRS['CURRENT_JSON_FOLDER'], ENDPOINTS['financial_list'], 'tickers_financial_info.json')
        print("tickers_financial_info created")
    except FileExistsError:
        print("tickers_financial_info already exist")

if not os.path.exists(TICKERS_PATH['tradeble_tickers']):
    try:
        FmpTickers.create_tickers_list(
            DIRS['CURRENT_JSON_FOLDER'], ENDPOINTS['tradeble_list'], 'tradeble_tickers.json')
        print("tradeble_tickers created")
    except FileExistsError:
        print("tradeble_tickers already exist")

if not os.path.exists(TICKERS_PATH['symbols']):
    try:
        FmpTickers.create_tickers_list(
            DIRS['CURRENT_JSON_FOLDER'],  ENDPOINTS['stock_list'], 'symbols.json')
        print("symbols created")

    except FileExistsError as e:
        print("symbols already exist")

if not os.path.exists(TICKERS_PATH['forex_pairs']):
    try:
        FmpTickers.create_tickers_list(
            DIRS['CURRENT_JSON_FOLDER'],  ENDPOINTS['forex_pairs'], 'forex_pairs.json')
        print("forex_pairs file created")

    except FileExistsError as e:
        print("forex_pairs file already exist")
