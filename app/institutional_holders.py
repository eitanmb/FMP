import sys
sys.path.append("..")

from config.endpoints import ENDPOINTS
from config.setup import DIRS, TICKERS_PATH
from helpers import FmpAPI
from helpers import utilities as util

def init() -> None:

    BASE_FOLDER = DIRS['CURRENT_JSON_FOLDER']
    tickers_list = FmpAPI.get_tickers_list(TICKERS_PATH['tickers_financial_info'])
    inst_holders:object = {
        'tickers_list': tickers_list,
        'endpoint': ENDPOINTS['holders'],
        'folder': f'{BASE_FOLDER}/institutional-holders-originales',
        'domain': 'holders'
    }
    data_name: str = "Institutional Holders"

    util.print_message( util.set_init_time( data_name ) )
    FmpAPI.download_companies_data(inst_holders)
    util.print_message( util.set_end_time( data_name ) )

if __name__ == "__main__":
    init()
