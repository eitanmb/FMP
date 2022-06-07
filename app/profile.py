from helpers import utilities as util
from helpers.FmpAPI import FmpAPI
from helpers import db_basics as db
from db.db_definitions import TABLE_PROFILE_STRUCTURE, PROFILE_INDEXES
from config.setup import DIRS, CONNECTION, TICKERS_PATH
from config.endpoints import ENDPOINTS
import sys
sys.path.append("..")


def init() -> None:
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    tickers_list = FmpAPI.get_tickers_list(TICKERS_PATH['symbols'])
    company_profile: object = {
        'tickers_list': tickers_list,
        'endpoint': ENDPOINTS['profile'],
        'table': 'profile',
        'folder': f'{BASE_FOLDER}/profiles',
        'domain': 'profile'
    }
    engine = db.engine_connetion(CONNECTION)

    def get_profile() -> None:
        db.execute_query(
            f"DROP TABLE IF EXISTS { company_profile['table'] }", engine)
        db.execute_query(TABLE_PROFILE_STRUCTURE, engine)
        db.execute_query(PROFILE_INDEXES, engine)
        FmpAPI.download_companies_data(company_profile)
        db.creat_dataframe_from_data(
            company_profile['folder'], engine, company_profile['table'])

    data_name: str = "Company Profile"
    util.print_messages(util.set_init_time(data_name))
    get_profile()
    util.print_messages(util.set_end_time(data_name))

if __name__ == "_main__":
    init()
