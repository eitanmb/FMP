import sys
sys.path.append("..")

from config.endpoints import ENDPOINTS
from config.setup import DIRS, CONNECTION, TICKERS_PATH
from db.db_definitions import PROFILE_DROP_TABLE, PROFILE_CREATE_TABLE, PROFILE_INDEXES
from helpers import db_basics as db
from helpers import utilities as util
from helpers.FmpAPI import FmpAPI

def init() -> None:
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    tickers_list = FmpAPI.get_tickers_list(TICKERS_PATH['symbols'])
    profile: object = {
        'domain': 'profile',
        'tickers_list': tickers_list,
        'endpoint': ENDPOINTS['profile'],
        'folder': f'{BASE_FOLDER}/profiles',
        'table': 'profile',
        'db_operations': {
            "drop_table": PROFILE_DROP_TABLE,
            "create_table": PROFILE_CREATE_TABLE,
            "indexes": PROFILE_INDEXES,
        }
    }
    engine = db.engine_connetion(CONNECTION)

    def create_profile_table():
        db.execute_query(profile['db_operations']['drop_table'], engine)
        db.execute_query(profile['db_operations']['create_table'], engine)

    def alter_profile_table():
        db.execute_query(profile['db_operations']['indexes'], engine)

    def get_profile() -> None:
        create_profile_table()
        alter_profile_table()
        FmpAPI.download_companies_data(profile)
        db.creat_dataframe_from_data(profile['folder'], engine, profile['table'])

    data_name: str = "Company Profile"
    util.print_messages(util.set_init_time(data_name))
    get_profile()
    util.print_messages(util.set_end_time(data_name))
    util.print_messages("Tiempo de ejecución", util.set_end_time(data_name) - util.set_init_time(data_name))

if __name__ == "_main__":
    init()
