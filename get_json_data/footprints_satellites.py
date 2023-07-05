import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# open a browser
# options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
browser = webdriver.Chrome()
# browser.get("https://satbeams.com/footprints?position=359")


'''
获取所有经度节点之后去重 
'''


def get_all_available_position_method2():
    browser.get("https://satbeams.com/footprints")
    available_position = []
    # 点击8次+45度
    for i in range(8):
        # 获取当前页面的经度节点
        longitude_list = browser.find_elements(By.XPATH, '//div[@class="paint"]/a')
        # 将经度节点添加到列表中
        for longitude in longitude_list:
            # 获取实际经度
            available_position.append(int(longitude.get_attribute('id')[2:-2]))
        # 点击下一页
        browser.find_element(by=By.XPATH, value='//div[@id="sat_bar"]/div[3]/a').click()
        available_position = list(set(available_position))
        available_position.sort()
    return available_position


'''
获取第一个a标签和最后一个a标签，读到最后一个a标签时停止
记录最后一个a标签的id
点击下一页
从上述记录的id开始读取,重复以上步骤
直到最后一个a标签的id和记录的id相同    
'''


def get_all_available_position_method1():
    browser.get("https://satbeams.com/footprints")
    available_position = []

    # 获取当前页面的经度节点
    number = browser.find_element(by=By.XPATH, value='//div[@class="paint"]/a]').get_attribute("id")
    start_id = number[2:-2]
    end_id = number[2:-2]
    # 设置起始指针
    available_position.append(start_id)
    available_position.append(end_id)
    # 判断是否成环
    while (start_id != end_id):
        # 获取当前页面的经度节点
        browser.find_element(by=By.XPATH, value='//div[@class="paint"]/a').get_attribute("id")[2:-2]
        # 将精度节点添加到列表中
        available_position.append('')
        # 更新end_id
        end_id = browser.find_element(by=By.XPATH, value='//div[@class="paint"]/a[last()]').get_attribute("id")[2:-2]
        # 点击下一页
        browser.find_element(by=By.XPATH, value='//div[@id="sat_bar"]/div[3]/a').click()
    return available_position


if __name__ == '__main__':
    # 获取所有可用的经度节点
    available_position = get_all_available_position_method2()
    # 依照顺序访问每一个经度节点
    longitude_dict = {}
    sat_number_total = 0
    for pos in available_position:
        browser.get("https://satbeams.com/footprints?position=" + str(pos))
        # 设置延时请求
        browser.implicitly_wait(5)
        # 获取该精度下的卫星数量
        sat_number = browser.find_elements(by=By.XPATH, value='//div[@id="beams_bar"]/table/tbody/tr/td')
        sat_number_total += len(sat_number)
        sat_dict = {}
        for sat in sat_number:
            spot_list = []
            # 获取卫星名字
            legend = sat.find_elements(by=By.XPATH, value='.//legend/a')
            sat_name = legend[0].text
            spots = sat.find_elements(by=By.XPATH, value='.//td/a')
            # 遍历该卫星下的可视点
            for spot in spots:
                spot_dict = {}
                # 查找缩略图地址
                spot_alias = spot.find_element(by=By.XPATH, value='./img').get_attribute('src')
                # 获取别名
                spot_alias = spot_alias[40:-7]
                spot_name = str(spot.text)
                spot_dict['spot_name'] = spot_name
                spot_dict['spot_alias'] = spot_alias
                # print(spot_name)
                spot_list.append(spot_dict)
            # 卫星名字和可视点数组存入字典
            sat_dict[sat_name] = spot_list
            # 使用json.dumps()方法将每个卫星下的可视地点数组转化为json
            json.dumps(spot_list)
        # 经度和对应卫星数组存入字典
        longitude_dict[str(pos)] = sat_dict
        json.dumps(longitude_dict)
    print(sat_number_total)
    longitude_dict = {str(key_sort): longitude_dict[str(key_sort)] for key_sort in
                      sorted(list(map(int, longitude_dict.keys())))}
    with open('footprints_satellites_1.json', 'w+') as f:
        json.dump(longitude_dict, f, indent=2)
    browser.close()


