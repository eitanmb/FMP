import os
import sys
sys.path.append("..")

from .FmpAPI import FmpAPI
from config.setup import TICKERS_PATH


class DataDownload(FmpAPI):
    def __init__(self, **kwargs):
        self.domain = kwargs['domain']
        self.endpoint = kwargs['endpoint']
        self.folder = kwargs['folder']
        self.tickers_path = TICKERS_PATH[kwargs['tickers_list']]
        self.store_ticket_list()

    def store_ticket_list(self):
        self.tickers_list = FmpAPI.get_tickers_list(self.tickers_path)

    def create_folder(self):
        try:
            print(os.makedirs(self.folder))
        except FileExistsError as error:
            print(error)

    def fetch_data(self):
        FmpAPI.download_companies_data({
            'domain':self.domain,
            'tickers_list':self.tickers_list,
            'endpoint':self.endpoint,
            'folder':self.folder,
        })
