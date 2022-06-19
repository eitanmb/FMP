import sys
sys.path.append("..")

from sql.definitions import IS_OPERATIONS, BS_OPERATIONS, CF_OPERATIONS, PROFILE_OPERATIONS
from .endpoints import ENDPOINTS
from .setup import DIRS
from  .types import types
BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']

profile_kwargs = {
    'domain':'profile',
    'tickers_list': types['stock_tickers'],
    'endpoint': ENDPOINTS['profile'], 
    'folder': f'{BASE_FOLDER}/profiles',
    'table': 'profile',
    'db_operations': PROFILE_OPERATIONS
}

income_statements_kwargs = {
    'domain':'IS',
    'tickers_list': types['fin_tickers'],
    'endpoint': ENDPOINTS['IS'], 
    'folder': f'{BASE_FOLDER}/financials/IS',
    'table': 'incomeStatement',
    'db_operations': IS_OPERATIONS
}

balance_sheet_kwargs = {
    'domain':'BS',
    'tickers_list': types['fin_tickers'],
    'endpoint': ENDPOINTS['BS'], 
    'folder': f'{BASE_FOLDER}/financials/BS',
    'table': 'balanceSheet',
    'db_operations': BS_OPERATIONS
}

cash_flow_kwargs = {
    'domain':'CF',
    'tickers_list': types['fin_tickers'],
    'endpoint': ENDPOINTS['CF'], 
    'folder': f'{BASE_FOLDER}/financials/CF',
    'table': 'cashFlow',
    'db_operations': CF_OPERATIONS
}
