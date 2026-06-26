import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger()

driver = webdriver.Edge()


def get_data():
    url = "https://taobao.com/"
    driver.get(url)
    time.sleep(2)

    search = driver.find_element(By.ID, 'q')
    search.send_keys("苹果手表")
    time.sleep(1)

    button = driver.find_element(By.CLASS_NAME, 'bth-search tb-bg')
    button.click()
    time.sleep(1)

#测试commit
