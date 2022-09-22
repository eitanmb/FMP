import sys
sys.path.append("..")

from config.currency import setup
from core.currency import currency_api

def init(DIRS):
    setup.init(DIRS)

    currency_api.init(setup.CURRENCIES_PAIRS, setup.DATE)