import sys
sys.path.append("..")

from .FmpAPI import FmpAPI
from config.setup import TICKERS_PATH
from config.dir_structure import make_directory


class DataDownload(FmpAPI):
    def __init__(self, **kwargs):
        self.domain = kwargs['domain']
        self.endpoint = kwargs['endpoint']
        self.folder = kwargs['folder']
        self.tickers_list =  FmpAPI.get_tickers_list(TICKERS_PATH[kwargs['tickers_list']])

    def create_folder(self):
        make_directory(self.folder)

    def fetch_data(self):
        FmpAPI.download_companies_data({
            'domain':self.domain,
            'tickers_list':self.tickers_list,
            'endpoint':self.endpoint,
            'folder':self.folder,
        })
