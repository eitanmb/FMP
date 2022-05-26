from dotenv import load_dotenv
import json
import os
import pandas as pd
import re
from urllib.request import urlopen
import sys

#Custom modules
from helpers.file_basics import *
from helpers.db_basics import create_table_from_dataframe
from helpers.utilities import *

load_dotenv()
apikey = os.environ.get("APIKEY")
url_base = os.environ.get("FMP_URL_BASE")
last_ticker = 'lastTicker.txt'


def create_tickers_list_with_financial_info(PATH: str) -> None:
    #Tradeble symbol List with financial statement
    write_json_file(f"{PATH}/tickers_financial_info.json", get_jsonparsed_data(url_base + f"/v3/financial-statement-symbol-lists?apikey={apikey}"))


def create_tradeble_tickers_list(PATH: str) -> None:
    #Tradeble symbol List with financial statement
    tickers_list = []
    for elemento in get_jsonparsed_data(url_base + f"/v3/available-traded/list?apikey={apikey}"):
        tickers_list.append(elemento['symbol'])

    write_json_file(f"{PATH}/tradeble_tickers.json",tickers_list)


def create_symbol_list(PATH: str) -> None:
    #All symbols
    tickers_list = []
    for elemento in get_jsonparsed_data(url_base + f"/v3/stock/list?apikey={apikey}"):
        tickers_list.append(elemento['symbol'])

    write_json_file(f"{PATH}/symbols.json", tickers_list)


def get_tickers_list(file):
    return json.load(open(file))


def get_jsonparsed_data(url: str):
    
    response = urlopen(url)
    data = response.read().decode("utf-8")

    return json.loads(data)


def get_fmp_data( tickers_list: list, partial_url: str, folder: str, caller: str ) -> None:
    data = []
    how_many_tickers = count_files_in_folder(folder)

    # Si el script falla podemos iniciar el bucle for desde este valor
    if how_many_tickers == 0:
        _from = 0 
    else:
        # _from = read_file(last_ticker)  
        _from = get_lastTicker_info(last_ticker)
        _from = int(_from[1])

    print( f"How many tickers= { how_many_tickers }" )
    print(f"Desde: {_from}")

    for i in range( _from, len(tickers_list) ):
         #eliminar caracteres no deseados
        ticker = re.sub("[\^\/]", "", tickers_list[i])

        if( caller == "outlook" or caller == "floatshares"):
            url = f"{partial_url}{ticker}&apikey={apikey}"
        else:
            url = f"{partial_url}{ticker}?apikey={apikey}"
        
        print(url)

        #write file with downloaded data
        file = f"{folder}/{ticker}.json"

        try:
            data = get_jsonparsed_data(url)

            if type(data) is list:
                if len(data) > 0:
                    write_json_file(file, data)
                else:
                    print(f"No data para { ticker }")
            
            elif(isinstance(data, dict)):
                if not "Not found! Please check the symbol" in data.values():
                    write_json_file(file, data)                
                else:
                    print(f"Not found! Please check the symbol {ticker}")
        
        except Exception as e:
            print(e, url)

        finally:
            #Guardar la posicion que tiene el ticker dentro de la tickers_list
            ticker_position = tickers_list.index(ticker)
            write_lastTicker_file(last_ticker, caller, ticker_position)
            
            print('ticker', ticker)

            how_many_tickers += 1
            print('How many: ', how_many_tickers)



def creat_dataframe_from_data ( folder: str, engine, table_name: str ):

    count = 1
    for file in files_in_folder(folder):
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