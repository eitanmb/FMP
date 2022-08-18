import sys
sys.path.append("..")


from datetime import datetime
import json
import pandas as pd
from selenium.webdriver.common.by import By
import time

from config.investing.inv_scraping_setup import INV_URLS, AVAILABLE_PAIRS, SCRAP_FX, SCRAP_POPUP_PROMO, fx_date_range
from helpers.File import File
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
    
    

def close_popup_promo_modal(driver):
    element = driver.find_element(By.XPATH, SCRAP_POPUP_PROMO["close"])
    element.click()
    


def set_fx_date_range(driver, main_window):
    if driver is None:
        return None
    
    try:
        return select_fx_date_range_from_calendar(driver, main_window)
    
    except Exception as error:
        print('ERROR::: ', error)
        driver.switch_to.window(main_window)
        return select_fx_date_range_from_calendar(driver, main_window)
        # close_popup_promo_modal(driver)
        # print(driver.current_window_handle)

    
    if  driver.current_window_handle != main_window:
        driver.switch_to.window(main_window)
        return select_fx_date_range_from_calendar(driver, main_window)



def change_fx_date_format(values):
    data = values.copy()

    for element in data:
        date = datetime.strptime(element[1], '%m/%d/%Y')
        date_formated = date.strftime('%Y-%m-%d')
        element[1] = date_formated
    
    return data



def build_dataframe_from_table(pair, doc):
    
    header = [ th for th in doc.xpath( SCRAP_FX["price_table"]["theader_th"] )]
    values = [[td for td in tr.xpath( SCRAP_FX["price_table"]["tbody_td"] )]  
                for tr in doc.xpath( SCRAP_FX["price_table"]["tbody_tr"] )]

    header.insert(0, "Pair")
    for element in values:
        element.insert(0,pair)
    values.pop()

    data = change_fx_date_format(values)
    return pd.DataFrame(data, columns=header)



def init(DIRS):
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    PATH:str = f"{BASE_FOLDER}/forex/"
    url_prefix = f"{INV_URLS['base']}{INV_URLS['fx']}"

    for currency in AVAILABLE_PAIRS:
        base_currency = currency[0]
        quote_currency = currency[1]
        pair = base_currency + quote_currency
        file = f"{PATH}{pair}.json"
        url = f"{url_prefix}/{base_currency.lower()}-{quote_currency.lower()}-historical-data"
        
        print(pair)
        print(url)

        driver = driver_init(url)
        main_window = driver.current_window_handle

        query_driver = set_fx_date_range(driver, main_window)
        doc = get_doc_from_url(query_driver)

        if driver is None:
            print(f"ERROR - NO HAY DATOS SOBRE {currency[0]} en Investing")
        
        driver.quit()
        currencydata = build_dataframe_from_table(pair, doc)
        print(currencydata)

        result = currencydata.to_json(orient="records")
        parsed = json.loads(result)
        File.write_json(file, parsed)
        
        print(json.dumps(parsed, indent=4))
