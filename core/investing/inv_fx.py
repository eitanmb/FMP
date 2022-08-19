import sys
sys.path.append("..")


from datetime import datetime
import json
import pandas as pd
from selenium.webdriver.common.by import By
import time

from config.investing.inv_scraping_setup import INV_URLS, AVAILABLE_PAIRS, SCRAP_FX, fx_date_range, TRACKER_FILE
from helpers.File import File
from helpers.utilities import return_start_from_tickers, get_download_ticker_possition, write_lastTicker_file, print_messages
from helpers.scraping_utilities import driver_init, get_doc_from_url

def select_fx_date_range_from_calendar(driver, main_window):
    
    while (driver.current_window_handle == main_window):
        element = driver.find_element(By.CLASS_NAME, SCRAP_FX["pick_calendar"])
        element.click()

        start_date = driver.find_element(By.XPATH, SCRAP_FX["start_date"])
        start_date.send_keys(fx_date_range["start"])
        
        end_date = driver.find_element(By.XPATH, SCRAP_FX["end_date"])
        end_date.send_keys(fx_date_range["end"])

        apply_date_range = driver.find_element(By.XPATH, SCRAP_FX["apply_date_range"])
        apply_date_range.click()

        time.sleep(2)
        break

    return driver
    
    

def set_fx_date_range(driver, main_window):
    if driver is None:
        return None
    
    try:
        return select_fx_date_range_from_calendar(driver, main_window)
    
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
        print_messages('length', len(value))
        if len(value) < 7:
            value.insert(5, 'Null')
        value.insert(0,pair)
    
    values.pop()



def build_dataframe_from_table(pair, doc):
    header = [ th for th in doc.xpath( SCRAP_FX["price_table"]["theader_th"] )]
    values = [[td for td in tr.xpath( SCRAP_FX["price_table"]["tbody_td"] )]  
                for tr in doc.xpath( SCRAP_FX["price_table"]["tbody_tr"] )]

    insert_pair_into_header(header)
    normalized_currency_values_data(values, pair)

    data = change_fx_date_format(values)
    return pd.DataFrame(data, columns=header)



def init(DIRS):
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    FOLDER:str = f"{BASE_FOLDER}/forex/"
    url_prefix = f"{INV_URLS['base']}{INV_URLS['fx']}"
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
        file = f"{FOLDER}{pair}.json"
        url = f"{url_prefix}/{base_currency.lower()}-{quote_currency.lower()}-historical-data"
        
        if File.file_exist(file):
            print_messages(f"{file} exist, continue next pair")
            continue

        print_messages('Downloading:', pair)
        print_messages('Pair URL:', url)

        try:
            driver = driver_init(url)
            main_window = driver.current_window_handle
            query_driver = set_fx_date_range(driver, main_window)
            doc = get_doc_from_url(query_driver)

            if driver is None:
                print(f"ERROR - NO HAY DATOS SOBRE {pair} en Investing")
            
            driver.quit()
            currencydata = build_dataframe_from_table(pair, doc)
            result = currencydata.to_json(orient="records")
            parsed = json.loads(result)
            File.write_json(file, parsed)
            how_many_tickers += 1
            print_messages(pair, "has been downloaded")
       
        except Exception as error:
            print_messages("ERROR:", error, pair)

        finally:
            ticker_position = get_download_ticker_possition(AVAILABLE_PAIRS, (base_currency, quote_currency))
            write_lastTicker_file(TRACKER_FILE,'fx', ticker_position)
            print_messages('How many: ', how_many_tickers)