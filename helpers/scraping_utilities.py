import sys
sys.path.append("..")

from helpers.utilities import print_messages
from bs4 import BeautifulSoup
from lxml import etree
import re
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


def is_404(driver):
    if re.search('Error 404: Page Not Found',driver.page_source):
        driver.quit()
        return True
    
    return False



def driver_init(url):
    firefox_options = Options()
    firefox_options.add_argument("-incognito")
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    driver.get(url)

    if is_404(driver) == True:
        print_messages("Error 404 - Página no encontrada: ", url)
        return None
    
    return driver




def get_doc_from_url(driver):
    if driver is None:
        return None

    html = driver.page_source.encode('utf-8')
    bs = BeautifulSoup(html,'html.parser')
    doc = etree.HTML(str(bs))
    return doc