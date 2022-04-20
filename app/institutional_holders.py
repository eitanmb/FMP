import sys
sys.path.append("..")

from config.setup import DIRS, TICKERS_PATH
from helpers.get_data_functions import *
from helpers.utilities import *

def init() -> None:

    BASE_FOLDER = DIRS['CURRENT_JSON_FOLDER']
    folder: str = f"{BASE_FOLDER}/institutional-holders-originales"
    data_name: str = "Institutional Holders"


    print( set_init_time( data_name ) )

    # GET Tradeble tickers
    tickers_list = get_tickers_list(TICKERS_PATH['tickers_financial_info'])

    #Preconfiurar url para obtener profiles
    inthoder_url =  f"{url_base}/v3/institutional-holder/"

    get_fmp_data( tickers_list, inthoder_url, folder, 'holders' )

    print( set_init_time( data_name ), set_end_time( data_name ) )


if __name__ == "__main__":
    init()
