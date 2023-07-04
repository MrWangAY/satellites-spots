from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

url = 'http://www.ptpress.com.cn'
# 创建一个 Chrome 浏览器实例
driver = webdriver.Firefox()
# 打开 Google 首页
driver.get(url)
# print(driver.current_window_handle)# 获取当前窗口句柄
driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[1]/div/div[2]/div[3]/input").send_keys(
    "python教程")
driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[1]/div/div[2]/div[3]/button").click()#找到对应按钮后进行点击功能
# 获取当前全部窗口句柄集合
handles=driver.window_handles
driver.switch_to.window(handles[-1])
print(driver.find_element(by=By.XPATH,value="/html/body/div[4]/div[2]/div/div").text)#获取对应元素的内容
time.sleep(10 )#设置页面何时关闭
driver.quit() #关闭一个窗口
# driver.close()//关闭浏览器

