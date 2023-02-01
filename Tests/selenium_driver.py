from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from time import sleep,time
from pathlib import Path

TIMEOUT = 5
TEST_DIR = str(Path(__file__).parent.resolve())
ATTEMPTS = 3

def chrome_driver(url):
    driver = Browser_driver("chrome")
    driver.get(url)
    driver.find_and_click(By.ID, "details-button")
    driver.find_and_click(By.ID, "proceed-link")
    return driver

def firefox_driver(url):
    driver = Browser_driver("firefox")
    driver.get(url)
    driver.find_and_click(By.ID, "advancedButton")
    driver.find_and_click(By.ID, "exceptionDialogButton")
    return driver

class Browser_driver():
    def __init__(self,browser):
        if browser not in ("chrome","firefox"):
            raise NotImplementedError
        options = Options()
        #options.add_argument('--headless')
        if browser == "chrome":
            self.driver = webdriver.Chrome("chromedriver", options=options)
        elif browser == "firefox":
            raise NotImplementedError
            self.driver = webdriver.Chrome("geckodriver", options=options)

    def get(self, url):
        self.driver.get(url)

    def close(self,):
        self.driver.close()

    def find_and_click(self, by, attribute):
        end_time = time()+TIMEOUT
        while True:
            try:
                elem = self.driver.find_element(by, attribute)
                if not elem.is_displayed():
                    continue
                elem.click()
                return elem
            except Exception as e:
                if time() > end_time:
                    raise e

    def find_and_send(self, by, attribute, data):
        end_time = time()+TIMEOUT
        while True:
            try:
                elem = self.driver.find_element(by, attribute)
                if not elem.is_displayed():
                    continue
                elem.send_keys(data)
                return elem
            except Exception as e:
                if time() > end_time:
                    raise e

    def get_inner_html(self, by, attribute):
        end_time = time()+TIMEOUT
        while True:
            try:
                elem = self.driver.find_element(by, attribute)
                if not elem.is_displayed():
                    continue
                return elem.get_attribute('innerHTML')
            except Exception as e:
                if time() > end_time:
                    raise e

