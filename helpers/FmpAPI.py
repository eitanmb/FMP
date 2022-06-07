from dotenv import load_dotenv
import json
import os
import pandas as pd
import re
from urllib.request import urlopen

# Custom modules
from helpers.File import File
from helpers import utilities as util
from config.endpoints import ENDPOINTS

load_dotenv()


class FmpAPI:
    apikey = os.environ.get("APIKEY")
    url_base = os.environ.get("FMP_URL_BASE")
    last_ticker = 'lastTicker.txt'

    @staticmethod
    def get_jsonparsed_data(url: str):
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    @staticmethod
    def get_tickers_list(file):
        return json.load(open(file))

    @staticmethod
    def get_path_to_file(PATH: str, file: str):
        return f"{PATH}/{file}"

    @staticmethod
    def configure_endpoint(endpoint, ticker=""):
        if ticker == "":
            return endpoint.format(url_base=FmpAPI.url_base, apikey=FmpAPI.apikey)
        return endpoint.format(url_base=FmpAPI.url_base, ticker=ticker, apikey=FmpAPI.apikey)
    
    @staticmethod
    def append_ticker(tickers):
        tickers_list = []
        for ticker in tickers:
            tickers_list.append(ticker['symbol'])
        return tickers_list

    
    @staticmethod
    def are_financial_tickers(endpoint):
        return endpoint.find("financial")

    @staticmethod
    def create_tickers_list(PATH: str, partial_endpoint:str, file_name:str):
        endpoint = FmpAPI.configure_endpoint(partial_endpoint)
        tickers = FmpAPI.get_jsonparsed_data(endpoint)
        path_to_file = FmpAPI.get_path_to_file(PATH, file_name)

        if  FmpAPI.are_financial_tickers(endpoint) == -1:
            tickers_list = FmpAPI.append_ticker(tickers)
            File.write_json(path_to_file, tickers_list)
        else:
            File.write_json(path_to_file, tickers)

    @staticmethod
    def clean_ticker(ticker):
        return re.sub("[\^\/]", "", ticker)

    @staticmethod
    def return_start_from_tickers(how_many_tickers):
        # Si el script falla podemos iniciar el bucle for desde este valor
        if how_many_tickers == 0:
            return 0
        return int(util.get_lastTicker_info(FmpAPI.last_ticker)[1])

    @staticmethod
    def does_not_exist(data):
        return "Not found! Please check the symbol" in data.values()

    @staticmethod
    def is_valid_data(data):
        if (util.is_list(data) and util.is_not_empty(data)) or \
                (util.is_dict(data) and FmpAPI.does_not_exist(data) == False):
            return True
        else:
            return False

    @staticmethod
    def get_download_ticker_possition(tickers_list, ticker):
        return tickers_list.index(ticker)

    @staticmethod
    def download_companies_data(domain) -> None:
        tickers_list = domain["tickers_list"]
        folder = domain[folder]
        partial_endpoint = domain["endpoint"]
        caller = domain["domain"]
        how_many_tickers = File.count_files_in_folder(folder)
        _from = FmpAPI.return_start_from_tickers(how_many_tickers)

        util.print_messages("How many tickers:", how_many_tickers)
        util.print_messages("Desde:", _from)

        for i in range(_from, len(tickers_list)):
            ticker = FmpAPI.clean_ticker(tickers_list[i])
            file = FmpAPI.get_path_to_file(folder, f"{ticker}.json")
            endpoint = FmpAPI.configure_endpoint(partial_endpoint, ticker)
            util.print_messages(endpoint)

            try:
                data = FmpAPI.get_jsonparsed_data(endpoint)
                if FmpAPI.is_valid_data(data):
                    File.write_json_file(file, data)
                else:
                    util.print_messages("No existe el ticker:", ticker)

            except Exception as error:
                util.print_messages(error, endpoint)

            finally:
                # Guardar la posicion que tiene el ticker dentro de la tickers_list
                ticker_position = FmpAPI.get_download_ticker_possition(
                    tickers_list, ticker)
                util.write_lastTicker_file(FmpAPI.last_ticker,
                                      caller, ticker_position)
                util.print_messages('ticker', ticker)
                how_many_tickers += 1
                util.print_messages('How many: ', how_many_tickers)
