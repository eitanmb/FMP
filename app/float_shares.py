import sys
sys.path.append("..")

from config.setup import DIRS, TICKERS_PATH
from helpers.get_data_functions import *
from helpers.utilities import *


def init() -> None:

    BASE_FOLDER = DIRS['CURRENT_JSON_FOLDER']
    folder: str = f"{BASE_FOLDER}/shares"
    data_name: str = "Float Shares"
    
    print( set_init_time( data_name ) )

    tickers_list = get_tickers_list(TICKERS_PATH['tickers_financial_info'])

    float_url =  f"{ url_base }/v4/shares_float?symbol="

    get_fmp_data( tickers_list, float_url, folder, 'floatshares' )

    print( set_init_time( data_name ), set_end_time( data_name ) )



if __name__ == "__main__":
    init()
