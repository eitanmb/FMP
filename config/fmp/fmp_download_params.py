import sys
sys.path.append("..")

# from sql.definitions_legacy_fmp import IS_OPERATIONS, BS_OPERATIONS, CF_OPERATIONS, PROFILE_OPERATIONS, FX_OPERATIONS
from noSql.definitions import PROFILE_NOSQl, IS_NOSQl, BS_NOSQl, CF_NOSQl, OUTLOOK_NOSQL
from .fmp_endpoints import ENDPOINTS
from .fmp_variables import holder_dates_available
from sql.definitions import IS_OPERATIONS, BS_OPERATIONS, CF_OPERATIONS, PROFILE_OPERATIONS, FX_OPERATIONS, OWNERSHIP_OPERATIONS


def init(DIRS, TICKERS_FILES):
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    # BASE_FOLDER: str = '/home/eitan/Programacion/FMP_2/json/2022/06'

    profile_kwargs = {
        'domain':'profile',
        'tickers_list': TICKERS_FILES['stock']['path_to_file'],
        'endpoint': ENDPOINTS['profile'], 
        'dates_available': None,
        'folder': f'{BASE_FOLDER}/profiles',
        'sql': PROFILE_OPERATIONS,
        'noSql': PROFILE_NOSQl
    }

    income_statements_kwargs = {
        'domain':'IS',
        'tickers_list': TICKERS_FILES['financial']['path_to_file'],
        'endpoint': ENDPOINTS['IS'], 
        'dates_available': None,
        'folder': f'{BASE_FOLDER}/financials/IS',
        'sql': IS_OPERATIONS,
        'noSql': IS_NOSQl
    }

    balance_sheet_kwargs = {
        'domain':'BS',
        'tickers_list': TICKERS_FILES['financial']['path_to_file'],
        'endpoint': ENDPOINTS['BS'], 
        'dates_available': None,
        'folder': f'{BASE_FOLDER}/financials/BS',
        'sql': BS_OPERATIONS,
        'noSql': BS_NOSQl
    }

    cash_flow_kwargs = {
        'domain':'CF',
        'tickers_list': TICKERS_FILES['financial']['path_to_file'],
        'endpoint': ENDPOINTS['CF'],
        'dates_available': None, 
        'folder': f'{BASE_FOLDER}/financials/CF',
        'sql': CF_OPERATIONS,
        'noSql': CF_NOSQl
    }

    ownership_kwargs = {
    'domain':'ownership',
    'tickers_list': TICKERS_FILES['stock']['path_to_file'],
    'endpoint': ENDPOINTS['stock_ownership'], 
    'dates_available': holder_dates_available,
    'folder': f'{BASE_FOLDER}/ownership',
    'sql': OWNERSHIP_OPERATIONS,
    'noSql': None
    }

    outlook_kwargs = {
        'domain':'outlook',
        'tickers_list': TICKERS_FILES['financial']['path_to_file'],
        'endpoint': ENDPOINTS['outlook'], 
        'dates_available': None,
        'folder': f'{BASE_FOLDER}/outlook',
        'sql': None,
        'noSql': OUTLOOK_NOSQL
    }

    forex_kwargs = {
        'domain':'forex',
        'tickers_list': TICKERS_FILES['forex']['path_to_file'],
        'endpoint': ENDPOINTS['forex'], 
        'dates_available': None,
        'folder': f'{BASE_FOLDER}/forex',
        'sql': FX_OPERATIONS,
        'noSql': None
    }



    return {
        "profile_kwargs": profile_kwargs,
        "income_statements_kwargs": income_statements_kwargs,
        "balance_sheet_kwargs":balance_sheet_kwargs,
        "cash_flow_kwargs":cash_flow_kwargs,
        "ownership_kwargs": ownership_kwargs,
        "outlook_kwargs":outlook_kwargs,
        "forex_kwargs":forex_kwargs,

    }