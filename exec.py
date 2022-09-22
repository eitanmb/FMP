from config import setup
from app import fmp_app
from app import currency_app

DIRS = setup.init()
currency_app.init(DIRS)
# fmp_app.init(DIRS)