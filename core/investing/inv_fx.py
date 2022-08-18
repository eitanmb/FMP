import sys
sys.path.append("..")

from bs4 import BeautifulSoup
from config.investing.available_pairs import available_pairs
from config.investing.inv_scraping_setup import base_url
from datetime import datetime
from lxml import etree
from selenium.webdriver.common.by import By
import json
import pandas as pd
import time

from  helpers.File import File
from helpers.scraping_utilities import driver_init


def select_date_range_from_calendar(driver, main_window, date_range):
    
    while (driver.current_window_handle == main_window):
        element = driver.find_element(By.CLASS_NAME, "DatePickerWrapper_icon__2w6rl")
        element.click()

        start_date = driver.find_element(By.XPATH, "//div[@class='NativeDateRangeInput_root__30aM8']//input[@type='date']")
        start_date.send_keys(date_range["start"])
        
        end_date = driver.find_element(By.XPATH, "//div[@class='NativeDateInput_root__27QxI']//following-sibling::div//input[@type='date']")
        end_date.send_keys(date_range["end"])

        apply = driver.find_element(By.XPATH,"//button[contains(@class,'apply-button__3sdPK')]")
        apply.click()

        time.sleep(2)
        break
    return driver
    
    

def close_popup_promo_modal(driver):
    element = driver.find_element(By.XPATH, "//i[@class='popupCloseIcon largeBannerCloser']")
    element.click()
    


def set_date_range(driver, main_window, date_range):

    if driver is None:
        return None

    try:
        return select_date_range_from_calendar(driver, main_window, date_range)
    
    except Exception as error:
        print('ERROR::: ', error)
        driver.switch_to.window(main_window)
        return select_date_range_from_calendar(driver, main_window, date_range)
        # close_popup_promo_modal(driver)
        # print(driver.current_window_handle)

    
    if  driver.current_window_handle != main_window:
        driver.switch_to.window(main_window)
        return select_date_range_from_calendar(driver, main_window, date_range)



def get_doc_from_url(driver):
    if driver is None:
        return None

    html = driver.page_source.encode('utf-8')
    bs = BeautifulSoup(html,'html.parser')
    doc = etree.HTML(str(bs))
    return doc


def change_date_format(values):
    data = values.copy()

    for element in data:
        date = datetime.strptime(element[1], '%m/%d/%Y')
        date_formated = date.strftime('%Y-%m-%d')
        element[1] = date_formated
    
    return data

def build_dataframe_from_table(pair, doc):
    
    header = [ th for th in doc.xpath('//table[contains(@data-test,"historical")]/thead/tr/th//span/text()')]
    values = [[td for td in tr.xpath('td//text()')]  
            for tr in doc.xpath('//table[contains(@data-test,"historical")]/tbody/tr')]

    header.insert(0, "Pair")
    for element in values:
        element.insert(0,pair)
    values.pop()

    data = change_date_format(values)
    return pd.DataFrame(data, columns=header)



def init(DIRS):
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']
    PATH:str = f"{BASE_FOLDER}/forex/"
    currecies_url = "/currencies/"
    #formato web investing: yyyy/mm/dd
    date_range = {
        "start": "2021-01-15",
        "end":"2021-02-22"
    }
    

    for currency in available_pairs:
        base_currency = currency[0]
        quote_currency = currency[1]
        pair = base_currency + quote_currency
        file = f"{PATH}{pair}.json"
        print(pair)
    
        url = f"{base_url}/{currecies_url}{base_currency.lower()}-{quote_currency.lower()}-historical-data"
        print(url)

        driver = driver_init(url)
        main_window = driver.current_window_handle

        query_driver = set_date_range(driver, main_window, date_range)
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
        # sys.exit()
