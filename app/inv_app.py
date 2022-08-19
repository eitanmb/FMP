import sys
sys.path.append("..")

from core.investing import inv_fx
from core.DataPersistenceNoSQL import NoSqlDataPersistence


def init(DIRS):
    inv_fx.init(DIRS)