import sys
sys.path.append("..")

from core.investing import get_currencies_exchange

def init(DIRS):
    get_currencies_exchange.init(DIRS)