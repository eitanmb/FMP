import sys
from tkinter import E
sys.path.append("..")

from config.endpoints import ENDPOINTS
from config.setup import DIRS, TICKERS_PATH
from helpers.utilities import *
from helpers import FmpAPI


def init() -> None:

  BASE_FOLDER = DIRS['CURRENT_JSON_FOLDER']
  folder: str = f"{BASE_FOLDER}/outlook"
  data_name: str = "Company Outlook"
  tickers_file = TICKERS_PATH['tickers_financial_info']
  tickers_list: list = FmpAPI.get_tickers_list(tickers_file)

  outlook: object = {
    'domain': 'outlook',
    'tickers_list': tickers_list,
    'endpoint': ENDPOINTS['outlook'],
    'folder': folder
  }

  print(set_init_time(data_name))

  FmpAPI.get_data(outlook)

  print( set_init_time( data_name ), set_end_time( data_name ) )


if __name__ == "_main__":
  init()
