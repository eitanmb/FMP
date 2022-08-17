from config import setup
import fmp_app

DIRS = setup.init()
fmp_app.init(DIRS)