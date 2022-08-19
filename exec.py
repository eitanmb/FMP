from config import setup
from app import fmp_app
from app import inv_app

DIRS = setup.init()
fmp_app.init(DIRS)
inv_app.init(DIRS)