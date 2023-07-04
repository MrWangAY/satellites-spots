import json
import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from selenium.webdriver.common.by import By

# open a browser
# options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
browser = webdriver.Chrome()
# browser.get("https://satbeams.com/footprints?position=359")

if __name__ == '__main__':
    browser.get("https://www.satbeams.com/packages")
    satellites = []
    # 获取当前页面的经度节点

    number = browser.find_elements(by=By.XPATH, value='//*[@id="sat_grid"]/tbody//tr[@class="class_tr"]/td[5]/a')
    for n in number:
        print(n.text)

        satellites.append(n.text)

    satellites = list(set(satellites))
    print(len(satellites))

