import json

from selenium import webdriver
from selenium.webdriver.common.by import By

# open a browser
# options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
browser = webdriver.Chrome()
# browser.get("https://satbeams.com/footprints?position=359")

if __name__ == '__main__':
    browser.get("https://www.satbeams.com/satellites?status=active")
    satellites = {}
    # 获取当前页面的经度节点

    number = browser.find_elements(by=By.XPATH, value='//*[@id="sat_grid"]/tbody//tr[@class="class_tr"]')
    for n in number:
        spots = n.find_elements(by=By.XPATH, value='.//td[2]')[0].text
        # 进行位置转化（便于记录和后续处理）
        if spots[-1] == 'W':
            spots = str(360 - int(spots[0:-2]))
        elif spots[-1] == 'E':
            spots = str(int(spots[0:-2]))
        # 初始化数组
        if satellites.get(spots) == None:
            satellites[spots] = []

        sat_name = n.find_elements(by=By.XPATH, value='.//td[4]')[0].text
        # 字符串截取，去除（）中描述内容且便于后续数据分析进行匹配
        if "(" in sat_name and ")" in sat_name:
            start_index = sat_name.index("(")
            end_index = sat_name.index(")")
            sat_name = sat_name.replace(sat_name[start_index:end_index + 1], "").strip()

        satellites[spots].append(sat_name)
    # 按照键进行字典排序
    satellites = {str(key_sort): satellites[str(key_sort)] for key_sort in sorted(list(map(int, satellites.keys())))}
    with open('active_satellites.json', 'w+', encoding='utf-8') as f:
        json.dump(satellites, f, indent=2)
    browser.close()

