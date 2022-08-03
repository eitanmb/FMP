import sys
sys.path.append("..")

from sql.definitions import IS_OPERATIONS, BS_OPERATIONS, CF_OPERATIONS, PROFILE_OPERATIONS
from .endpoints import ENDPOINTS
from .setup import DIRS, TICKERS_FILES
from helpers.utilities import get_year, get_month


BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
_date: str = f"{get_month()}{get_year()}"

# BASE_FOLDER: str = '/home/eitan/Programacion/FMP_2/json/2022/07'
# _date: str = "072022"

profile_kwargs = {
    'domain':'profile',
    'tickers_list': TICKERS_FILES['stock']['path_to_file'],
    'endpoint': ENDPOINTS['profile'], 
    'folder': f'{BASE_FOLDER}/profiles',
    'sql': PROFILE_OPERATIONS,
    'noSql': {
        'collection_name':f'{_date}_profile'
    }
}

income_statements_kwargs = {
    'domain':'IS',
    'tickers_list': TICKERS_FILES['financial']['path_to_file'],
    'endpoint': ENDPOINTS['IS'], 
    'folder': f'{BASE_FOLDER}/financials/IS',
    'sql': IS_OPERATIONS,
    'noSql': {
        'collection_name':f'{_date}_incomeStatements'
    }
}

balance_sheet_kwargs = {
    'domain':'BS',
    'tickers_list': TICKERS_FILES['financial']['path_to_file'],
    'endpoint': ENDPOINTS['BS'], 
    'folder': f'{BASE_FOLDER}/financials/BS',
    'sql': BS_OPERATIONS,
    'noSql': {
        'collection_name':f'{_date}_balanceSheet'
    }
}

cash_flow_kwargs = {
    'domain':'CF',
    'tickers_list': TICKERS_FILES['financial']['path_to_file'],
    'endpoint': ENDPOINTS['CF'], 
    'folder': f'{BASE_FOLDER}/financials/CF',
    'sql': CF_OPERATIONS,
    'noSql': {
        'collection_name':f'{_date}_cashFlow'
    }
}

outlook_kwargs = {
    'domain':'outlook',
    'tickers_list': TICKERS_FILES['financial']['path_to_file'],
    'endpoint': ENDPOINTS['outlook'], 
    'folder': f'{BASE_FOLDER}/outlook',
    'sql': None,
    'noSql': {
        'collection_name':f'{_date}_outlook'
    }
}

forex_kwargs = {
    'domain':'forex',
    'tickers_list': TICKERS_FILES['forex']['path_to_file'],
    'endpoint': ENDPOINTS['forex'], 
    'folder': f'{BASE_FOLDER}/forex',
    'sql': None,
    'noSql': None
}
