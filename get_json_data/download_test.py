from selenium import webdriver
import time
import re
from selenium.webdriver.common.action_chains import ActionChains


browser = webdriver.Chrome()
# BASE_DOMAIN = 'https://pixabay.com/zh/images/search/?order=ec'
BASE_DOMAIN = 'https://pixabay.com/images/search/?pagi='  # 目标网站
for j in range(2, 30):
    browser.get(BASE_DOMAIN + str(j))

    text = browser.page_source  # 获取页面信息
    pattern = re.compile(r'<a class="link--h3bPW" href="(.*?)" data-id="(.*?)">')
    res = re.findall(pattern, text)  # 正则表达式匹配

    browser.get(res[0][0])

    for i in res:
        browser.get(i[0])
        time.sleep(3)
        pic = browser.find_element_by_xpath('//picture//img')
        action = ActionChains(browser).move_to_element(pic)  # 移动到该元素
        action.context_click(pic)  # 右键点击该元素
        action.perform()  # 执行

       #
        time.sleep(10)
browser.close()


