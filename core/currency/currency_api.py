import requests
import sys
import time
sys.path.append("..")

from helpers.File import File
from helpers.currency_utilities import *


def get_historical_exchange_by_pair(date, pair):
    url = f"https://currency-converter5.p.rapidapi.com/currency/historical/{date}"

    querystring = {"from":"USD","amount":"1","format":"json","to":f"{pair}"}

    headers = {
        "X-RapidAPI-Key": "917edfaa46mshe1c92ce766bdd64p1457a6jsn102bd286b04b",
        "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)



def init(CURRENCIES_PAIRS, DATE):
    load_currencies = File.read_json(CURRENCIES_PAIRS["path_to_file"])
    dates_list = get_dates_in_between(DATE["starting_date"], DATE["n_days"], "days")
    
    for currency in load_currencies:
        for date in dates_list:
            get_historical_exchange_by_pair(date, currency[1])
            time.sleep(2)

