import os
import sys
sys.path.append("..")

from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from sql.db_basics import *
from core.FmpAPI import FmpAPI
from helpers.utilities import *
from config.setup import CONNECTION


def init():
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Actual API key is stored in a .env file.  Not good to store API key directly in script.
    load_dotenv()
    apikey = os.environ.get("APIKEY")
    url_base = "https://financialmodelingprep.com/api/v3/"
    table_name = "forex"
    engine = engine_connetion(CONNECTION)

    # Get all FOREX PAIR available
    # url_fx_all = url_base + f"symbol/available-forex-currency-pairs?apikey={apikey}"
    url_fx_all = url_base + \
        f"symbol/available-forex-currency-pairs?apikey={apikey}"

    fx_pairs = FmpAPI.get_jsonparsed_data(url_fx_all)
    pairs = []

    for pair in fx_pairs:

        if pair['currency'] == "USD" and pair['symbol'].find('USD') != -1:
            pairs.append(pair['symbol'])

    print('Pares disponibles: ', pairs)
    print('Pares disponibles: ', len(pairs))

    # Get USD PAIR FOREX HISTORIC VALUES
    fx_values = []
    fx_values_temp = []

    for pair in pairs:
        url_fx = url_base + f"historical-price-full/{pair}?apikey={apikey}"
        fx_values_temp.append(FmpAPI.get_jsonparsed_data(url_fx))
        fx_values.append(fx_values_temp)
        fx_values_temp = []

    # CREAR LISTA DE VALORES QUE SERVIRA DE DATA PARA DATAFRAME
    values_list = []
    values_list_temp = []
    for fx_value in fx_values:
        try:
            for i in range(0, len(fx_value[0]['historical'])):
                values_list_temp.append(fx_value[0]['symbol'])
                values_list_temp.append(fx_value[0]['historical'][i]['date'])
                values_list_temp.append(fx_value[0]['historical'][i]['close'])

                # print(values_list_temp)
                values_list.append(values_list_temp)
                values_list_temp = []

        except Exception as e:
            print(e)

    # CREAR dataframe
    df = pd.DataFrame(data=values_list, columns=['pair', 'date', 'close'])

    # Escribir en la BD
    execute_query(f'DROP TABLE IF EXISTS {table_name}', engine)
    print(create_table_from_dataframe(df, engine, table_name))

    print(f"Final: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    init()
