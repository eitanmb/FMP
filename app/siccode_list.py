try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import os
import sys
import typing
import fmpsdk
import json
from datetime import datetime
import time
from helpers.db_basics import engine_connetion, create_table_from_dataframe, execute_query
from helpers.get_data_functions import *
from helpers.utilities import *
from helpers.file_basics import *

#Variables globales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
folder: str      = f"{BASE_DIR}/json/sic/code-by-company/"

def init():

    #INIT
    inicio = f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print( inicio )

    # GET Tradeble tickers
    tickers_list = get_tickers_list('json/tickers.json')

    #Preconfiurar url para obtener profiles
    partial_url =  f"{url_base}v4/standard_industrial_classification?symbol="

    # print(partial_url)
    # sys.exit()

    get_fmp_data( tickers_list, partial_url, folder, 'sic_codes' )


    final = f"Final: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print( inicio, final )



init()
