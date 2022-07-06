import sys
sys.path.append("..")

from sql.definitions import IS_OPERATIONS, BS_OPERATIONS, CF_OPERATIONS, PROFILE_OPERATIONS
from .endpoints import ENDPOINTS
from .setup import DIRS, TICKERS_FILES
BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']

profile_kwargs = {
    'domain':'profile',
    'tickers_list': TICKERS_FILES['stock']['path_to_file'],
    'endpoint': ENDPOINTS['profile'], 
    'folder': f'{BASE_FOLDER}/profiles',
    'sql': PROFILE_OPERATIONS
}

income_statements_kwargs = {
    'domain':'IS',
    'tickers_list': TICKERS_FILES['financial']['path_to_file'],
    'endpoint': ENDPOINTS['IS'], 
    'folder': f'{BASE_FOLDER}/financials/IS',
    'sql': IS_OPERATIONS
}

balance_sheet_kwargs = {
    'domain':'BS',
    'tickers_list': TICKERS_FILES['financial']['path_to_file'],
    'endpoint': ENDPOINTS['BS'], 
    'folder': f'{BASE_FOLDER}/financials/BS',
    'sql': BS_OPERATIONS
}

cash_flow_kwargs = {
    'domain':'CF',
    'tickers_list': TICKERS_FILES['financial']['path_to_file'],
    'endpoint': ENDPOINTS['CF'], 
    'folder': f'{BASE_FOLDER}/financials/CF',
    'sql': CF_OPERATIONS
}

outlook_kwargs = {
    'domain':'outlook',
    'tickers_list': TICKERS_FILES['financial']['path_to_file'],
    'endpoint': ENDPOINTS['outlook'], 
    'folder': f'{BASE_FOLDER}/outlook',
    'sql': None
}
