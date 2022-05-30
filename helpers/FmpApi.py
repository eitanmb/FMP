from dotenv import load_dotenv
import json
import os
import pandas as pd
import re
from urllib.request import urlopen

#Custom modules
from helpers import File 
from helpers.db_basics import create_table_from_dataframe
from helpers.utilities import *

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
    def create_tickers_list_with_financial_info(PATH: str) -> None:
        #Tradeble symbol List with financial statement
        File.write_json(f"{PATH}/tickers_financial_info.json", FmpAPI.get_jsonparsed_data(FmpAPI.url_base + f"/v3/financial-statement-symbol-lists?apikey={FmpAPI.apikey}"))
    
    @staticmethod
    def create_tradeble_tickers_list(PATH: str) -> None:
        #Tradeble symbol List with financial statement
        tickers_list = []
        for elemento in FmpAPI.get_jsonparsed_data(FmpAPI.url_base + f"/v3/available-traded/list?apikey={FmpAPI.apikey}"):
            tickers_list.append(elemento['symbol'])

        File.write_json(f"{PATH}/tradeble_tickers.json",tickers_list)

    @staticmethod
    def create_symbol_list(PATH: str) -> None:
        #All symbols
        tickers_list = []
        for elemento in FmpAPI.get_jsonparsed_data(FmpAPI.url_base + f"/v3/stock/list?apikey={FmpAPI.apikey}"):
            tickers_list.append(elemento['symbol'])

        File.write_json(f"{PATH}/symbols.json", tickers_list)

    @staticmethod
    def get_tickers_list(file):
        return json.load(open(file))

    @staticmethod
    def get_data(domain) -> None:
        tickers_list = domain.tickers_list
        folder = domain.folder
        partial_url = domain.url
        caller = domain.domain
        data = []
        how_many_tickers = File.count_files_in_folder(folder)

        # Si el script falla podemos iniciar el bucle for desde este valor
        if how_many_tickers == 0:
            _from = 0 
        else:
            # _from = read_file(last_ticker)  
            _from = get_lastTicker_info(FmpAPI.last_ticker)
            _from = int(_from[1])

        print( f"How many tickers= { how_many_tickers }" )
        print(f"Desde: {_from}")

        for i in range( _from, len(tickers_list) ):
            #eliminar caracteres no deseados
            ticker = re.sub("[\^\/]", "", tickers_list[i])

            if( caller == "outlook" or caller == "floatshares"):
                url = f"{partial_url}{ticker}&apikey={FmpAPI.apikey}"
            else:
                url = f"{partial_url}{ticker}?apikey={FmpAPI.apikey}"
            
            print(url)

            #write file with downloaded data
            file = f"{folder}/{ticker}.json"

            try:
                data = FmpAPI.get_jsonparsed_data(url)

                if type(data) is list:
                    if len(data) > 0:
                        File.write_json(file, data)
                    else:
                        print(f"No data para { ticker }")
                
                elif(isinstance(data, dict)):
                    if not "Not found! Please check the symbol" in data.values():
                        File.write_json(file, data)                
                    else:
                        print(f"Not found! Please check the symbol {ticker}")
            
            except Exception as e:
                print(e, url)

            finally:
                #Guardar la posicion que tiene el ticker dentro de la tickers_list
                ticker_position = tickers_list.index(ticker)
                write_lastTicker_file(FmpAPI.last_ticker, caller, ticker_position)
                
                print('ticker', ticker)

                how_many_tickers += 1
                print('How many: ', how_many_tickers)

    @staticmethod
    def creat_dataframe_from_data ( folder: str, engine, table_name: str ):

        count = 1
        for file in File.files_in_folder(folder):
            print(f"Counter financials = {count}")

            try:
                df = pd.read_json(f"{folder}/{file}", orient='columns')

                if df.empty == False:
                    print( file, df )
                    print(create_table_from_dataframe( df, engine, table_name ))
                else:
                    print("Dataframe vacío")

            except Exception as e:
                print(e)

            count += 1