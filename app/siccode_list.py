import os
from datetime import datetime
from helpers.db_basics import engine_connetion, create_table_from_dataframe, execute_query
from helpers import FmpAPI
from helpers.utilities import *
from helpers.File import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
folder: str      = f"{BASE_DIR}/json/sic/code-by-company/"

def init():

    inicio = f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print( inicio )

    tickers_list = FmpAPI.get_tickers_list('json/tickers.json')

    partial_url =  f"{FmpAPI.url_base}v4/standard_industrial_classification?symbol="

    FmpAPI.get_data( tickers_list, partial_url, folder, 'sic_codes' )

    final = f"Final: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print( inicio, final )



init()
