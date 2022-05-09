import sys
sys.path.append("..")

from config.setup import DIRS, CONNECTION, TICKERS_PATH
from db.db_definitions import TABLE_PROFILE_STRUCTURE, PROFILE_INDEXES
from helpers.db_basics import engine_connetion, execute_query
from helpers.get_data_functions import *
from helpers.utilities import *

def init() -> None:
  BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
  folder: str      = f"{BASE_FOLDER}/profiles"
  table_name: str  = "profile"
  data_name: str = "Company Profile"

  #Connexion con BBDD
  engine = engine_connetion(CONNECTION)

  def get_profile( tickers_list:list, profile_url:str, folder:str ) -> None:
      #Eliminar la tabla si existe
      
      execute_query(f'DROP TABLE IF EXISTS {table_name}', engine)
      execute_query( TABLE_PROFILE_STRUCTURE, engine )
      execute_query( PROFILE_INDEXES, engine )
      get_fmp_data(tickers_list, profile_url, folder, 'profile')
      creat_dataframe_from_data ( folder, engine, table_name )



  print( set_init_time( data_name ) )

  tickers_list = get_tickers_list(TICKERS_PATH['symbols'])

  profile_url =  f"{url_base}/v3/profile/"

  get_profile( tickers_list, profile_url, folder )

  print( set_init_time( data_name ), set_end_time( data_name ) )


if __name__ == "_main__":
  init()
