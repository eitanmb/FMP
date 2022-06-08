import sys
sys.path.append("..")
from tkinter import E

from config.endpoints import ENDPOINTS
from config.setup import DIRS, TICKERS_PATH
from helpers.FmpAPI import FmpAPI
from helpers import utilities as util


def init() -> None:

    BASE_FOLDER = DIRS['CURRENT_JSON_FOLDER']
    tickers_file = TICKERS_PATH['tickers_financial_info']
    tickers_list: list = FmpAPI.get_tickers_list(tickers_file)
    outlook: object = {
        'domain': 'outlook',
        'tickers_list': tickers_list,
        'endpoint': ENDPOINTS['outlook'],
        'folder': f"{BASE_FOLDER}/outlook"
    }

    data_name: str = "Company Outlook"
    util.print_messages(util.set_init_time(data_name))
    FmpAPI.download_companies_data(outlook)
    util.print_messages(util.set_end_time(data_name))
    util.print_messages("Tiempo de ejecución", util.set_end_time(data_name) - util.set_init_time(data_name))

if __name__ == "_main__":
    init()
