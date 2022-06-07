from helpers.utilities import *
from helpers.FmpAPI import FmpAPI
from helpers import db_basics as db
from db.db_definitions import IS_INDEXES, BS_INDEXES, CF_INDEXES
from config.endpoints import ENDPOINTS
from config.setup import DIRS, CONNECTION, TICKERS_PATH
import sys

sys.path.append("..")


def init(tipo_report: str) -> None:

    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    folder: str = f"{BASE_FOLDER}/financials"

    report: object = {

        "IS": {
            "endpoint": ENDPOINTS["IS"],
            "table": "incomeStatement",
            "domain": "Income Statement"
        },
        "BS": {
            "endpoint": ENDPOINTS["BS"],
            "table": "balanceSheet",
            "domain": "Balance Sheet"
        },
        "CF": {
            "endpoint": ENDPOINTS["CF"],
            "table": "cashFlow",
            "domain": "Cash Flow"
        }
    }

    tickers_list = FmpAPI.get_tickers_list(
        TICKERS_PATH['tickers_financial_info'])

    financial_report: object = {
        'tickers_list': tickers_list,
        'endpoint': report[tipo_report]['endpoint'],
        'table': report[tipo_report]['table'],
        'folder': f"{folder}/{tipo_report}/",
        'domain': tipo_report
    }
    engine = db.engine_connetion(CONNECTION)

    def get_financial_report():
        db.execute_query(
            f"DROP TABLE IF EXISTS {financial_report['table']}", engine)
        FmpAPI.download_companies_data(financial_report)
        db.creat_dataframe_from_data(
            financial_report['folder'], engine, financial_report['table'])

        if financial_report.domain == "IS":
            db.execute_query(IS_INDEXES, engine)
        if financial_report.domain == "BS":
            db.execute_query(BS_INDEXES, engine)
        if financial_report.domain == "CF":
            db.execute_query(CF_INDEXES, engine)

    data_name: str = report[tipo_report]['domain']
    print_messages(set_init_time(data_name))
    get_financial_report()
    print_messages(set_end_time(data_name))


if __name__ == "_main__":
    init()
