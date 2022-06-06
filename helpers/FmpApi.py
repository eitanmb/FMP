from dotenv import load_dotenv
import json
import os
import pandas as pd
import re
from urllib.request import urlopen

# Custom modules
from helpers import File
from helpers.db_basics import create_table_from_dataframe
from helpers.utilities import *
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
            return endpoint.format(utl_base=FmpAPI.url_base, api=FmpAPI.apikey)
        return endpoint.format(utl_base=FmpAPI.url_base, ticker=ticker, api=FmpAPI.apikey)

    @staticmethod
    def clean_ticker(ticker):
        return re.sub("[\^\/]", "", ticker)

    @staticmethod
    def create_tickers_list(PATH: str, partial_endpoint, file_name):
        endpoint = FmpAPI.configure_endpoint(partial_endpoint)
        tickers = FmpAPI.get_jsonparsed_data(endpoint)
        path_to_file = FmpAPI.get_path_to_file(PATH, file_name)

        tickers_list = []
        for ticker in tickers:
            tickers_list.append(ticker['symbol'])

        File.write_json(path_to_file, tickers_list)

    @staticmethod
    def return_start_from_tickers(how_many_tickers):
        # Si el script falla podemos iniciar el bucle for desde este valor
        if how_many_tickers == 0:
            return 0
        return int(get_lastTicker_info(FmpAPI.last_ticker)[1])

    @staticmethod
    def print_messages(*messages):
        print(*messages)

    @staticmethod
    def data_type_is_list(data):
        return type(data) is list

    @staticmethod
    def data_type_is_dict(data):
        return isinstance(data, dict)

    @staticmethod
    def is_not_empty_list(data):
        return len(data) > 0

    @staticmethod
    def symbol_does_not_exist(data):
        return "Not found! Please check the symbol" in data.values()

    @staticmethod
    def is_valid_data(data):
        if (FmpAPI.data_type_is_list(data) and FmpAPI.is_not_empty_list(data)) or \
                (FmpAPI.data_type_is_dict(data) and FmpAPI.symbol_does_not_exist(data) == False):
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

        FmpAPI.print_messages("How many tickers:", how_many_tickers)
        FmpAPI.print_messages("Desde:", _from)

        for i in range(_from, len(tickers_list)):
            ticker = FmpAPI.clean_ticker(tickers_list[i])
            file = FmpAPI.get_path_to_file(folder, f"{ticker}.json")
            endpoint = FmpAPI.configure_endpoint(partial_endpoint, ticker)
            FmpAPI.print_messages(endpoint)

            try:
                data = FmpAPI.get_jsonparsed_data(endpoint)
                if FmpAPI.is_valid_data(data):
                    

                FmpAPI.print_messages("No existe el ticker", ticker)

            except Exception as error:
                FmpAPI.print_messages(error, endpoint)

            finally:
                # Guardar la posicion que tiene el ticker dentro de la tickers_list
                ticker_position = FmpAPI.get_download_ticker_possition(
                    tickers_list, ticker)
                write_lastTicker_file(FmpAPI.last_ticker,
                                      caller, ticker_position)
                FmpAPI.print_messages('ticker', ticker)
                how_many_tickers += 1
                FmpAPI.print_messages('How many: ', how_many_tickers)

    @staticmethod
    def creat_dataframe_from_data(folder: str, engine, table_name: str):

        count = 1
        for file in File.files_in_folder(folder):
            print(f"Counter financials = {count}")

            try:
                df = pd.read_json(f"{folder}/{file}", orient='columns')

                if df.empty == False:
                    print(file, df)
                    print(create_table_from_dataframe(df, engine, table_name))
                else:
                    print("Dataframe vacío")

            except Exception as e:
                print(e)

            count += 1
