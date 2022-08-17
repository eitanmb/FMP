import sys
sys.path.append("..")

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time

def driver_init_headless(base_url, extende_url):
    base_url = "https://www.investing.com"
    firefox_options = Options()
    # firefox_options.add_argument("-incognito")
    # firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    url = base_url + extende_url
    driver.get(url)
    driver = verify_404(driver,url)
    time.sleep(3)
    return driver

def verify_404(driver,url):
    source = driver.page_source
    if re.search('Error 404: Page Not Found',source):
        print("Error 404 - Página no encontrada: {}".format(url))
        driver.quit() #cerrar driver Selenium
        driver = None
    return driver