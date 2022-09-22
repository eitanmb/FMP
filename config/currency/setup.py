import sys
sys.path.append("..")

from datetime import datetime
from helpers.currency_utilities import *
from helpers.utilities import *
from helpers.File import File
from .available_currencies import get_currency_list


starting_date = datetime.strptime("2010-01-01", "%Y-%m-%d")
ending_date = get_date()

delta = ending_date - starting_date

n_days =delta.days
n_years = n_days / 365
n_months = (n_days / 365) * 12
CURRENCIES_PAIRS = {}
DATE = {
    "starting_date":starting_date,
    "ending_date":ending_date,
    "n_days": n_days,
    "n_months": n_months,
    "n_years": n_years
}

def init(DIRS):
    CURRENCIES_PAIRS["file_name"] = 'currecy_pairs.json'
    CURRENCIES_PAIRS["path_to_file"] = f"{DIRS['CURRENT_JSON_FOLDER']}/currecy_pairs.json"
    
    currency_list = get_currency_list()
    currency_pairs = create_currency_pairs(currency_list)
    
    def create_currency_pair_json_file():
        if File.file_exist(CURRENCIES_PAIRS["path_to_file"]):
            return
        File.write_json(CURRENCIES_PAIRS["path_to_file"], currency_pairs)

    create_currency_pair_json_file()

