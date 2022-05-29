import sys

sys.path.append("..")

from config.setup import DIRS, CONNECTION, TICKERS_PATH
from db.db_definitions import IS_INDEXES, BS_INDEXES, CF_INDEXES
from helpers.db_basics import engine_connetion, execute_query
from helpers import FmpAPI
from helpers.utilities import *


def init( tipo_report:str ) -> None:
    
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    folder: str = f"{BASE_FOLDER}/financials"
    
    report: object = {

        # TODO: VERIFICAR SI NECESITAS mandar FmpAPI.url_base
        "IS": {
            "url":f"{FmpAPI.url_base}/v3/income-statement/",
            "table": "incomeStatement",
            "domain": "Income Statement"
        },
        "BS": {
            "url":f"{FmpAPI.url_base}/v3/balance-sheet-statement/",
            "table": "balanceSheet",
            "domain": "Balance Sheet"
        },
        "CF": {
            "url":f"{FmpAPI.url_base}/v3/cash-flow-statement/",
            "table": "cashFlow",
            "domain": "Cash Flow"
        }
    }

    tickers_list = FmpAPI.get_tickers_list(TICKERS_PATH['tickers_financial_info'])
    
    financial_report: object = {
        'tickers_list': tickers_list,
        'url': report[tipo_report]['url'],
        'table': report[tipo_report]['table'],
        'folder': f"{folder}/{tipo_report}/",
        'domain': tipo_report
    }

    engine = engine_connetion(CONNECTION)

    def get_financial_report():
        execute_query(f'DROP TABLE IF EXISTS {financial_report.table}', engine)
        FmpAPI.get_data(financial_report)
        FmpAPI.creat_dataframe_from_data(financial_report.folder, engine, financial_report.table)

        if financial_report.domain == "IS":
            execute_query( IS_INDEXES, engine )
        if financial_report.domain == "BS":
            execute_query( BS_INDEXES, engine )
        if financial_report.domain == "CF":
            execute_query( CF_INDEXES, engine )

    # END def get_financial
    
    data_name: str = report[tipo_report]['domain']
    print( set_init_time(data_name))

    get_financial_report()

    print( set_init_time( data_name ), set_end_time( data_name ) )


if __name__ == "_main__":
  init()