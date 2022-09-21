from selenium.webdriver.common.by import By
from config.investing.inv_scraping_setup import SCRAP_POPUP_PROMO


def close_popup_promo_modal(driver):
    element = driver.find_element(By.XPATH, SCRAP_POPUP_PROMO["close"])
    element.click()
    