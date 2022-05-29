import sys
sys.path.append("..")

from config.setup import DIRS, TICKERS_PATH
from helpers.utilities import *
from helpers import FmpAPI


def init() -> None:

  BASE_FOLDER = DIRS['CURRENT_JSON_FOLDER']
  folder: str = f"{BASE_FOLDER}/outlook"
  data_name: str = "Company Outlook"
  tickers_file = TICKERS_PATH['tickers_financial_info']
  url: str =  f"{FmpAPI.url_base}/v4/company-outlook?symbol="
  tickers_list: list = FmpAPI.get_tickers_list(tickers_file)

  outlook: object = {
    'tickers_list': tickers_list,
    'url': url,
    'folder': folder,
    'domain': 'outlook'
  }

  print(set_init_time(data_name))

  FmpAPI.get_data(outlook)

  print( set_init_time( data_name ), set_end_time( data_name ) )


if __name__ == "_main__":
  init()
