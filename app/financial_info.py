import sys
sys.path.append("..")

from config.setup import DIRS, CONNECTION, TICKERS_PATH
from db.db_definitions import IS_INDEXES, BS_INDEXES
from helpers.db_basics import engine_connetion, execute_query
from helpers.get_data_functions import *
from helpers.utilities import *


def init( tipo_report:str ) -> None:
    
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    folder: str      = f"{BASE_FOLDER}/financials"

    report_data: object = {
        "IS": {
            "url":f"{url_base}/v3/income-statement/",
            "table": "incomeStatement",
            "data_name": "Income Statement"
        },
        "BS": {
            "url":f"{url_base}/v3/balance-sheet-statement/",
            "table": "balanceSheet",
            "data_name": "Balance Sheet"
        },
        "CF": {
            "url":f"{url_base}/v3/cash-flow-statement/",
            "table": "cashFlow",
            "data_name": "Cash Flow"
        }
    }

    engine = engine_connetion(CONNECTION)

    def get_financial( finan_url: str, table_name: str, tickers_list: list, folder: str, report_type: str ):

        execute_query(f'DROP TABLE IF EXISTS {table_name}', engine)

        get_fmp_data( tickers_list, finan_url, folder, tipo_report )

        creat_dataframe_from_data ( folder, engine, table_name )

        execute_query( f'ALTER TABLE {table_name} ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (`id`)', engine )

        if report_type == "IS":
            execute_query( IS_INDEXES, engine )
        
        if report_type == "BS":
            execute_query( BS_INDEXES, engine )


        execute_query( f'ALTER TABLE {table_name} CHANGE COLUMN `link` `link{table_name.title()}` TEXT NULL DEFAULT NULL , \
                        CHANGE COLUMN `finalLink` `finalLink{table_name.title()}` TEXT NULL DEFAULT NULL ;', engine)


    # END def get_financial
    
    
    data_name: str = report_data[tipo_report]['data_name']
    
    print( set_init_time( data_name ) )

    tickers_list = get_tickers_list(TICKERS_PATH['tickers_financial_info'])

    get_financial( report_data[tipo_report]['url'], report_data[tipo_report]['table'], tickers_list, f"{folder}/{tipo_report}/", tipo_report )
    

    print( set_init_time( data_name ), set_end_time( data_name ) )




if __name__ == "_main__":
  init()