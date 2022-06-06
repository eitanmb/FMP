# from ast import List
import os
import sys
from helpers import FmpAPI
from helpers.db_basics import *
sys.path.append("..")

from config.directory_structure import *
from config.endpoints import ENDPOINTS


BASE_DIR: str = os.path.dirname(os.path.abspath( 'fmp') )

DIRS: object = {
  'ROOT_JSON_DIR': "",
  'CURRENT_JSON_FOLDER': ""
}
CONNECTION: object = {}
TICKERS_PATH: object = {}

DIRS['ROOT_JSON_DIR'] = f'{ BASE_DIR }/json'

subdirectories_list: list = []
date: str = get_date()
subdirectories_list = get_subdirectories_by_date( date )

# FOLDER STRUCTURE
def init() -> None:
  global DIRS
  global CONNECTION
  global TICKERS_PATH

  create_json_directory_structure( DIRS["ROOT_JSON_DIR"], subdirectories_list )
  
  
  if DIRS['CURRENT_JSON_FOLDER'] == "":
      DIRS['CURRENT_JSON_FOLDER'] = set_current_json_folder( DIRS['ROOT_JSON_DIR'], subdirectories_list )
    
  # DB CONNECTION DATA
  CONNECTION['user'] = 'eitan'
  CONNECTION['host'] = 'localhost'
  CONNECTION['password'] = '123456'
  CONNECTION['database'] = f'FMP_{ subdirectories_list[0] }_{ subdirectories_list[1] }'

  #CREATE DB IF NOT EXIST
  create_db(CONNECTION);

  
  #GET TICKERS LISTS
  TICKERS_PATH['tickers_financial_info'] = f'{ DIRS["CURRENT_JSON_FOLDER"] }/tickers_financial_info.json'
  TICKERS_PATH['tradable_tickers'] = f'{ DIRS["CURRENT_JSON_FOLDER"] }/tradeble_tickers.json'
  TICKERS_PATH['symbols'] = f'{ DIRS["CURRENT_JSON_FOLDER"] }/symbols.json'

   
  if not os.path.exists(TICKERS_PATH['tickers_financial_info']):
    try:
      FmpAPI.create_tickers_list( DIRS['CURRENT_JSON_FOLDER'],ENDPOINTS['financial_list'], 'tickers_financial_info.json')
      print("tickers_financial_info created")
    except FileExistsError:
      print("tickers_financial_info already exist")

  if not os.path.exists(TICKERS_PATH['tradable_tickers']):
    try:
      FmpAPI.create_tradeble_tickers_list(DIRS['CURRENT_JSON_FOLDER'], ENDPOINTS['tradeble_list'], 'tradable_tickers.json')
      print("tradable_tickers created")
    except FileExistsError:
      print("tradable_tickers already exist")

  if not os.path.exists(TICKERS_PATH['symbols']):
    try:
      FmpAPI.create_symbol_list(DIRS['CURRENT_JSON_FOLDER'],  ENDPOINTS['stock_list'], 'symbols.json')
      print("symbols created")
    
    except FileExistsError as e:
      print("symbols already exist")
    
  
  
  if __name__ == "__main__":
    init()

    