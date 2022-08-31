import sys
sys.path.append("..")


from datetime import datetime
import json
import re
import pandas as pd
from selenium.webdriver.common.by import By
import time

from config.investing import inv_scraping_setup
from helpers.File import File
from helpers.utilities import return_start_from_tickers, get_download_ticker_possition, write_lastTicker_file, print_messages, make_directory
from helpers.scraping_utilities import driver_init, get_doc_from_url

# TODO:
# ANTES de escribir los json files de cada pair, debe quitarse las comas en los precios y el % en la cabecera Change

def init(inputs):

    TRACKER_FILE = inputs['TRACKER_FILE']
    AVAILABLE_PAIRS = inputs['AVAILABLE_PAIRS']
    FOLDER = inputs['fx_kwargs']['folder']
    url_prefix = inputs['fx_kwargs']['url_prefix']
    scrap_rules = inputs['fx_kwargs']['scrap']
    date_range = inputs['fx_kwargs']['date_range']

    make_directory(FOLDER)

    #TEMPORAL - ESTO DEBE SER LLAMADO ABAJO: JUSTO ANTES DE ESCRIBIR EL ARCHIVO JSON
    # remove_commas_from_values_in_json_files(FOLDER)
    # remove_percent_symbol_from_json_files_header(FOLDER)
    sys.exit()

    how_many_tickers = File.count_files_in_folder(FOLDER)
    _from = 0
    
    if File.file_is_empty(TRACKER_FILE) == False:
       _from = return_start_from_tickers(how_many_tickers, TRACKER_FILE)

    print_messages("How many tickers:", how_many_tickers)
    print_messages("Desde:", _from)

    for i in range(_from, len(AVAILABLE_PAIRS)):
        base_currency = AVAILABLE_PAIRS[i][0]
        quote_currency = AVAILABLE_PAIRS[i][1]
        pair = base_currency + quote_currency
        file = f"{FOLDER}/{pair}.json"
        url = f"{url_prefix}/{base_currency.lower()}-{quote_currency.lower()}-historical-data"
        
        if File.file_exist(file):
            print_messages(f"{file} exist, continue next pair")
            continue

        print_messages('Downloading:', pair)
        print_messages('Pair URL:', url)

        try:
            driver = driver_init(url)
            main_window = driver.current_window_handle
            query_driver = set_fx_date_range(driver, main_window, date_range, scrap_rules)
            doc = get_doc_from_url(query_driver)

            if driver is None:
                print(f"ERROR - NO HAY DATOS SOBRE {pair} en Investing")
            
            driver.quit()
            currencydata = build_dataframe_from_table(pair, doc, scrap_rules)
            result = currencydata.to_json(orient="records")
            parsed = json.loads(result)
            
            # TODO: llamar aquí función de limpieza de comas y arreglo de cabecera

            File.write_json(file, parsed)
            
            how_many_tickers += 1
            print_messages(pair, "has been downloaded")
       
        except Exception as error:
            print_messages("ERROR:", error, pair)

        finally:
            ticker_position = get_download_ticker_possition(AVAILABLE_PAIRS, (base_currency, quote_currency))
            write_lastTicker_file(TRACKER_FILE,'fx', ticker_position)
            print_messages('How many: ', how_many_tickers)



def remove_commas_from_values_in_json_files(folder):
    replace_data = []

    for file in File.files_in_folder(folder):
        parsed_file = File.read_json(f"{folder}/{file}")
            
        for doc in parsed_file:
            for key, value in doc.items():
                if value and re.search("\,", value):
                    doc[key] = value.replace(",", "")
                    replace_data.append(doc)
            
        if len(replace_data) > 0:
            File.write_json(f"{folder}/{file}", replace_data)

        replace_data = []




def set_fx_date_range_from_calendar(driver, main_window, date_range, scrap_rules):
    
    while (driver.current_window_handle == main_window):
        element = driver.find_element(By.CLASS_NAME, scrap_rules["pick_calendar"])
        element.click()

        start_date = driver.find_element(By.XPATH, scrap_rules["start_date"])
        start_date.send_keys(date_range["start"])
        
        end_date = driver.find_element(By.XPATH, scrap_rules["end_date"])
        end_date.send_keys(date_range["end"])

        apply_date_range = driver.find_element(By.XPATH, scrap_rules["apply_date_range"])
        apply_date_range.click()

        time.sleep(2)
        break

    return driver
    
    

def set_fx_date_range(driver, main_window, date_range, scrap_rules):
    
    if driver is None:
        return None

    try:
        return set_fx_date_range_from_calendar(driver, main_window, date_range, scrap_rules)
    except Exception as error:
        print('ERROR::: ', error)
        print_messages('POPUP:', driver.current_window_handle)
        html = driver.page_source.encode('utf-8')
        File.write('popupSource.html', html)
        # driver.switch_to.window(main_window)
        # return select_fx_date_range_from_calendar(driver, main_window)


def insert_pair_into_header(header):
    header.insert(0, "Pair")



def change_fx_date_format(values):
    data = values.copy()

    for element in data:
        date = datetime.strptime(element[1], '%m/%d/%Y')
        date_formated = date.strftime('%Y-%m-%d')
        element[1] = date_formated
    
    return data



def normalized_currency_values_data(values, pair):
    for value in values:
        if len(value) < 7:
            value.insert(5, 'Null')
        value.insert(0,pair)
    
    values.pop()




def build_dataframe_from_table(pair, doc, scrap_rules):
    header = [ th for th in doc.xpath( scrap_rules["price_table"]["theader_th"] )]
    values = [[td for td in tr.xpath( scrap_rules["price_table"]["tbody_td"] )]  
                for tr in doc.xpath( scrap_rules["price_table"]["tbody_tr"] )]

    insert_pair_into_header(header)
    normalized_currency_values_data(values, pair)

    data = change_fx_date_format(values)
    return pd.DataFrame(data, columns=header)
