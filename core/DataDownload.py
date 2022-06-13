import sys
sys.path.append("..")

from .FmpAPI import FmpAPI
from config.setup import TICKERS_PATH
from config.directory_structure import make_directory


class DataDownload(FmpAPI):
    def __init__(self, domain, tickers_list, endpoint, folder, table=None, db_operations=None):
        self.domain = domain
        self.tickers_list =  FmpAPI.get_tickers_list(TICKERS_PATH[tickers_list])
        self.endpoint = endpoint
        self.folder = folder
        self.table = table
        self.db_operations = db_operations

    def create_folder(self):
        make_directory(self.folder)

    def fetch_data(self):
        FmpAPI.download_companies_data(self)
