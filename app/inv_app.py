import sys
sys.path.append("..")

from core.investing import inv_fx
from core.DataPersistenceNoSQL import NoSqlDataPersistence
from config.investing import inv_scraping_setup


def create_data_persistence_noSQL(kargs):
        noSql = NoSqlDataPersistence(**kargs)
        noSql.create_collection()
        noSql.insert_collection_data_from_json_files()
        noSql.create_indexes()

def init(DIRS):
    fx = inv_scraping_setup.init(DIRS)
    inv_fx.init(fx)
    create_data_persistence_noSQL(fx['fx_kwargs'])
    