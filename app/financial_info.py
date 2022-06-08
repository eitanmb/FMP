import sys
sys.path.append("..")

from config.endpoints import ENDPOINTS
from config.setup import DIRS, CONNECTION, TICKERS_PATH
from db.db_definitions import IS_INDEXES, BS_INDEXES, CF_INDEXES, \
    IS_FK, BS_FK, CF_FK, IS_DELETE_NO_SYMBOL, BS_DELETE_NO_SYMBOL, CF_DELETE_NO_SYMBOL, \
    IS_TABLE_STRUCTURE, BS_TABLE_STRUCTURE, CF_TABLE_STRUCTURE
from helpers.utilities import *
from helpers.FmpAPI import FmpAPI
from helpers import db_basics as db

def init(tipo_report: str) -> None:
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    folder: str = f"{BASE_FOLDER}/financials"

    report: object = {

        "IS": {
            "domain": "Income Statement",
            "endpoint": ENDPOINTS["IS"],
            "table": "incomeStatement",
            "db_operations": {
                "create_table": IS_TABLE_STRUCTURE,
                "indexes": IS_INDEXES,
                "delete_null": IS_DELETE_NO_SYMBOL,
                "fk": IS_FK
            }
        },
        "BS": {
            "domain": "Balance Sheet",
            "endpoint": ENDPOINTS["BS"],
            "table": "balanceSheet",
            "db_operations": {
                "create_table": BS_TABLE_STRUCTURE,
                "indexes": BS_INDEXES,
                "delete_null": BS_DELETE_NO_SYMBOL,
                "fk": BS_FK
            }
        },
        "CF": {
            "domain": "Cash Flow",
            "endpoint": ENDPOINTS["CF"],
            "table": "cashFlow",
            "db_operations": {
                "create_table": CF_TABLE_STRUCTURE,
                "indexes": CF_INDEXES,
                "delete_null": CF_DELETE_NO_SYMBOL,
                "fk": CF_FK
            }
        }
    }

    tickers_list = FmpAPI.get_tickers_list(
        TICKERS_PATH['tickers_financial_info'])

    financial_report: object = {
        'domain': tipo_report,
        'tickers_list': tickers_list,
        'endpoint': report[tipo_report]['endpoint'],
        'table': report[tipo_report]['table'],
        'folder': f"{folder}/{tipo_report}/",
        'db_operations': report[tipo_report]['db_operations']
    }
    engine = db.engine_connetion(CONNECTION)

    def drop_financial_report_table()-> None:
        db.execute_query(
            f"DROP TABLE IF EXISTS {financial_report['table']}", engine)

    def create_financial_report_table()-> None:
        db.execute_query(
            financial_report['db_operations']['create_table'], engine)

    def alter_financial_report_table()-> None:
        db.execute_query(financial_report['db_operations']['indexes'], engine)
        db.execute_query(
            financial_report['db_operations']['delete_null'], engine)
        db.execute_query(financial_report['db_operations']['fk'], engine)

    def get_financial_report()-> None:
        FmpAPI.download_companies_data(financial_report)
        drop_financial_report_table()
        create_financial_report_table()
        db.creat_dataframe_from_data(
            financial_report['folder'], engine, financial_report['table'])
        alter_financial_report_table()

    data_name: str = report[tipo_report]['domain']
    print_messages(set_init_time(data_name))
    get_financial_report()
    print_messages(set_end_time(data_name))

if __name__ == "_main__":
    init()
