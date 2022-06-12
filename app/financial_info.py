import sys
sys.path.append("..")

from db import db_basics as db
from core.FmpAPI import FmpAPI
from helpers.utilities import *
from db.db_definitions import IS_CHANGE_COLUMNS, BS_CHANGE_COLUMNS, CF_CHANGE_COLUMNS, \
    IS_FK, BS_FK, CF_FK, IS_DELETE_NO_SYMBOL, BS_DELETE_NO_SYMBOL, CF_DELETE_NO_SYMBOL, \
    IS_CREATE_TABLE, BS_CREATE_TABLE, CF_CREATE_TABLE, IS_DROP_TABLE, BS_DROP_TABLE, CF_DROP_TABLE
from config.setup import DIRS, CONNECTION, TICKERS_PATH
from config.endpoints import ENDPOINTS


def init(tipo_report: str) -> None:
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    engine = db.engine_connetion(CONNECTION)
    folder: str = f"{BASE_FOLDER}/financials"
    report: object = {
        "IS": {
            "domain": "Income Statement",
            "endpoint": ENDPOINTS["IS"],
            "table": "incomeStatement",
            "db_operations": {
                "drop_table": IS_DROP_TABLE,
                "create_table": IS_CREATE_TABLE,
                "alter": IS_CHANGE_COLUMNS,
                "delete_null": IS_DELETE_NO_SYMBOL,
                "fk": IS_FK
            }
        },
        "BS": {
            "domain": "Balance Sheet",
            "endpoint": ENDPOINTS["BS"],
            "table": "balanceSheet",
            "db_operations": {
                "drop_table": BS_DROP_TABLE,
                "create_table": BS_CREATE_TABLE,
                "alter": BS_CHANGE_COLUMNS,
                "delete_null": BS_DELETE_NO_SYMBOL,
                "fk": BS_FK
            }
        },
        "CF": {
            "domain": "Cash Flow",
            "endpoint": ENDPOINTS["CF"],
            "table": "cashFlow",
            "db_operations": {
                "drop_table": CF_DROP_TABLE,
                "create_table": CF_CREATE_TABLE,
                "alter": CF_CHANGE_COLUMNS,
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
        'folder': f"{folder}/{tipo_report}/",
        'table': report[tipo_report]['table'],
        'db_operations': report[tipo_report]['db_operations']
    }

    def execute_table_operation(action: str, message:str) -> None:
        result = db.execute_query(action, engine)
        print_messages(message, result)

    def get_financial_report() -> None:
        drop_table = financial_report['db_operations']['drop_table']
        create_table = financial_report['db_operations']['create_table']
        add_indexes = financial_report['db_operations']['fk']
        alter_table = financial_report['db_operations']['alter']
        folder = financial_report['folder']
        table = financial_report['table']

        execute_table_operation(drop_table, "Drop table:")
        execute_table_operation(create_table, "Create table:")
        execute_table_operation(add_indexes, "Create indexes:")
        FmpAPI.download_companies_data(financial_report)
        db.creat_dataframe_from_data(folder, engine, table)
        execute_table_operation(alter_table, "Alter table:")

    data_name: str = financial_report['domain']
    print_messages(set_init_time(data_name))
    get_financial_report()
    print_messages(set_end_time(data_name))


if __name__ == "_main__":
    init()