###Información histótica del valor de las monedas, obtenida de MARKETS INSIDERS###

import sys
from lxml import etree
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import json

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from available_pairs import available_pairs

currecies_url = "/currencies/"

#formato web investing: mm/dd/yyyy
_from = "01/01/2021"
_till = "02/01/2021"


def verify_404(driver,url):
    source = driver.page_source
    if re.search('Error 404: Page Not Found',source):
        print("Error 404 - Página no encontrada: {}".format(url))
        driver.quit() #cerrar driver Selenium
        driver = None
    return driver

def driver_init_headless(extende_url):
    base_url = "https://www.investing.com"
    firefox_options = Options()
    firefox_options.add_argument("-incognito")
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    url = base_url + extende_url
    driver.get(url)
    driver = verify_404(driver,url)
    time.sleep(3)
    return driver

def avoid_popup_promo(driver,main_window,by,argument):

    try:
        if by == "xpath":
            element = driver.find_element(By.XPATH, argument)
        elif by == "textlink":
            element = driver.find_element(By.LINK_TEXT, argument)

        element.click()

    except Exception as e:
        print(str(e))
        #Cerrar el popup window
        element = driver.find_element(By.XPATH, "//i[@class='popupCloseIcon largeBannerCloser']")
        # click the elementprnt
        element.click()
        #volver a la ventana principal
        driver.switch_to.window(main_window)
        time.sleep(5)
        #Seleccionar elemento
        if by == "xpath":
            element = driver.find_element(By.XPATH,argument)
        elif  by == "textlink":
            element = driver.find_element(By.LINK_TEXT,argument)

        element.click()
        # Obtener el codigo fuente de la nueva página
        time.sleep(5)

    finally:
        return driver


def select_date_calendar(url,_from,_till):
    # driver = driver_init(url)
    driver = driver_init_headless(url)

    if driver is not None:
        main_window = driver.current_window_handle
        try:
            #open calendar
            element = WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@id='widgetField']"))).click()
        except Exception as e:
            print(str(e))
            #Cerrar el popup window
            element = driver.find_element(By.XPATH, "//i[@class='popupCloseIcon largeBannerCloser']")
            # click the elementprnt
            element.click()
            #volver a la ventana principal
            driver.switch_to.window(main_window)
            time.sleep(5)
            #intentar de nuevo
            element = WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@id='widgetField']"))).click()
        try:
            start_date = driver.find_element(By.ID, "startDate")
            start_date.clear()
            start_date.send_keys(_from)
        except Exception as e:
            print(str(e))
            #Cerrar el popup window
            element = driver.find_element(By.XPATH, "//i[@class='popupCloseIcon largeBannerCloser']")
            # click the elementprnt
            element.click()
            #volver a la ventana principal
            driver.switch_to.window(main_window)
            time.sleep(5)
                #Intertar de nuevo
            element = WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@id='widgetField']"))).click()
            start_date = driver.find_element(By.ID,"startDate")
            start_date.clear()
            start_date.send_keys(_from)

        #write in the end date field
        try:
            end_date = driver.find_element(By.ID,"endDate")
            end_date.clear()
            end_date.send_keys(_till)
        except Exception as e:
            print(str(e))
            #Cerrar el popup window
            element = driver.find_element(By.XPATH, "//i[@class='popupCloseIcon largeBannerCloser']")
            # click the elementprnt
            element.click()
            #volver a la ventana principal
            driver.switch_to.window(main_window)
            time.sleep(5)

            #Intertar de nuevo
            element = WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@id='widgetField']"))).click()
            end_date = driver.find_element(By.ID,"endDate")
            end_date.end_date.clear()
            end_date.send_keys(_till)

        #Ok, a fechas en claendario
        try:
            element = driver.find_element(By.XPATH, "//a[@id='applyBtn']")
            # click the elementprnt
            element.click()
        except Exception as e:
            print(str(e))
            #Cerrar el popup window
            element = driver.find_element(By.XPATH, "//i[@class='popupCloseIcon largeBannerCloser']")
            # click the elementprnt
            element.click()
            #volver a la ventana principal
            driver.switch_to.window(main_window)
            time.sleep(5)
            #intentar de nuevo
            element = WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@id='widgetField']"))).click()
            element = driver.find_element(By.XPATH, "//a[@id='applyBtn']")
            element.click()

        time.sleep(6)
        return driver
    else:
        return None

def get_doc_from_url(driver):
    if driver is not None:
        html = driver.page_source.encode('utf-8')
        bs = BeautifulSoup(html,'html.parser')
        doc = etree.HTML(str(bs))
        return doc
    else:
        return None

def build_currecy_value_dataframe(pair, doc):
    head = doc.xpath('//table[@id="curr_table"]/thead//th/text()')
    # header = []
    header = ["Pair"]
    for h in head:
        h = h.title()
        header.append(h.strip())

    header.remove('Open')
    header.remove('High')
    header.remove('Low')
    header.remove('Change %')
    print(header)

    prices = doc.xpath('//table[@id="curr_table"]/tbody//td/text()')

    temp_prices = []
    final_prices = []

    if prices == []: #asegurarnos de que la lista contiene datos
        return

    count = 0
    for x in prices:
        if count < len(head):
            if count == 0:
                #corresponde a la fecha, convertirla al formato de la bbdd
                d = datetime.strptime(x, '%b %d, %Y')
                new_date = d.strftime('%Y-%m-%d')
                temp_prices.append(pair)
                temp_prices.append(new_date)
            elif count == 1:
                temp_prices.append(x)
            count+=1
        else:
            final_prices.append(temp_prices)
            temp_prices = []
            d = datetime.strptime(x, '%b %d, %Y')
            new_date = d.strftime('%Y-%m-%d')
            temp_prices.append(pair)
            temp_prices.append(new_date)
            count = 1

    final_prices.append(temp_prices)
    currencydata= pd.DataFrame(data=final_prices)
    currencydata.columns=header
    currencydata = currencydata.iloc[::-1]
    return currencydata


def read_json(file):
    jd = open(file)
    data = json.load(jd)
    return data

def write_json(file, data):
    with open(file, 'w') as fp:
        json.dump(data, fp)

path = '/home/eitan/'

def init():
    for currency in available_pairs:
        base_currency = currency[0]
        quote_currency = currency[1]
        pair = base_currency + quote_currency
        file = f"{path}{pair}.json"
        print(pair)
    
        extende_url = currecies_url + base_currency.lower() + '-' + quote_currency.lower() + "-historical-data"
        print(extende_url)

        driver = select_date_calendar(extende_url,_from,_till)
        doc = get_doc_from_url(driver)

        if driver is not None:
            driver.quit() #cerrar driver Selenium
            currencydata = build_currecy_value_dataframe(pair, doc)

            result = currencydata.to_json(orient="records")
            parsed = json.loads(result)
            write_json(file, parsed)
            
            print(json.dumps(parsed, indent=4))
            # sys.exit()
        else:
            print("ERROR - NO HAY DATOS SOBRE {} EN Investing\n\n".format(currency[0]))




if __name__ == "__main__":
    init()
