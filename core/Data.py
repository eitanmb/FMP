import sys
sys.path.append("..")
from config.setup import DIRS
from config.endpoints import ENDPOINTS


BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']


class Data:
    def __init__(self, domain, tickers_list, endpoint, folder, table=None, db_operations=None):
        self.domain = domain
        self.tickers_list = tickers_list
        self.endpoint = endpoint
        self.folder = folder
        self.table = table
        self.db_operations = db_operations


outlook = Data('outlook', 'mi_tickers_laist',
               ENDPOINTS['outlook'], f"{BASE_FOLDER}/outlook", "outlookTable")
print(outlook.table)
