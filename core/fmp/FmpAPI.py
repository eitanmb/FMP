from dotenv import load_dotenv
from urllib.request import urlopen
import json
import os
import re
import sys

from helpers import utilities as util
from helpers.File import File

load_dotenv()
'''
TODO: los parametros que deben pasarsele al endpoint depende de la versión del fmp endpoint. 
Evaluar si es más lógico utilizar ese parametro

'''


class FmpImplementation:

    def get_tickers_list(file):
        return json.load(open(file))

    def get_path_to_file(PATH: str, file: str):
        return f"{PATH}/{file}"

    def configure_endpoint(endpoint, ticker=""):
        if ticker == "":
            return endpoint.format(url_base=FmpAPI.url_base, apikey=FmpAPI.apikey)
        return endpoint.format(url_base=FmpAPI.url_base, ticker=ticker, apikey=FmpAPI.apikey)

    def does_not_exist(data):
        return "Not found! Please check the symbol" in data.values()

    def is_list(data):
        return type(data) is list

    def is_dict(data):
        return isinstance(data, dict)

    def is_not_empty(data):
        return len(data) > 0

    def is_valid_data(data):
        if (FmpImplementation.is_list(data) and FmpImplementation.is_not_empty(data)) or \
                (FmpImplementation.is_dict(data) and FmpImplementation.does_not_exist(data) == False):
            return True
        else:
            return False


class FmpTickers:
    def append_ticker(tickers):
        tickers_list = []
        for ticker in tickers:
            tickers_list.append(ticker['symbol'])
        return tickers_list

    def clean_ticker(ticker):
        return re.sub("[\^\/]", "", ticker)

    def are_financial_tickers(endpoint):
        return endpoint.find("statement")

    def create_tickers_list(path_to_file: str, partial_endpoint: str):
        endpoint = FmpImplementation.configure_endpoint(partial_endpoint)
        tickers = FmpAPI.get_jsonparsed_data(endpoint)

        if FmpTickers.are_financial_tickers(endpoint) == -1:
            tickers_list = FmpTickers.append_ticker(tickers)
            File.write_json(path_to_file, tickers_list)
        else:
            File.write_json(path_to_file, tickers)


class FmpAPI:
    apikey = os.environ.get("APIKEY")
    url_base = os.environ.get("FMP_URL_BASE")
    last_ticker = 'lastTicker.txt'

    def get_jsonparsed_data(url: str):
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    def return_start_from_tickers(how_many_tickers):
        if how_many_tickers == 0:
            return 0
        return int(util.get_lastTicker_info(FmpAPI.last_ticker)[1])

    def get_download_ticker_possition(tickers_list, ticker):
        return tickers_list.index(ticker)

    def download_companies_data(domain) -> None:
        tickers_list = domain["tickers_list"]
        folder = domain['folder']
        partial_endpoint = domain["endpoint"]
        caller = domain["domain"]
        how_many_tickers = File.count_files_in_folder(folder)
        _from = FmpAPI.return_start_from_tickers(how_many_tickers)

        util.print_messages("How many tickers:", how_many_tickers)
        util.print_messages("Desde:", _from)

        for i in range(_from, len(tickers_list)):
            ticker = FmpTickers.clean_ticker(tickers_list[i])
            file = FmpImplementation.get_path_to_file(folder, f"{ticker}.json")
            endpoint = FmpImplementation.configure_endpoint(
                partial_endpoint, ticker)
            util.print_messages(endpoint)

            try:
                data = FmpAPI.get_jsonparsed_data(endpoint)
                if FmpImplementation.is_valid_data(data):
                    File.write_json(file, data)
                else:
                    util.print_messages("No existe el ticker:", ticker)

            except Exception as error:
                util.print_messages(error, endpoint)

            finally:
                ticker_position = FmpAPI.get_download_ticker_possition(
                    tickers_list, ticker)
                util.write_lastTicker_file(FmpAPI.last_ticker,caller, ticker_position)
                util.print_messages('ticker', ticker)
                how_many_tickers += 1
                util.print_messages('How many: ', how_many_tickers)
