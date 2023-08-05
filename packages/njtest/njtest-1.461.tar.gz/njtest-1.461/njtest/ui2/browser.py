import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

'''
pip install Appium-Python-Client  安装WebDriverWait
https://blog.csdn.net/cz9025/article/details/70160273
'''


class Browser(object):
    __instance = None
    __first_init = False

    def __new__(cls, tips=True):  # 创建类对象时调用
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, tips=True):  # 创建成功调用
        '''
            电脑游览器控制
        :param tips:错误提示是否打开
        '''
        self.tips = tips
        if not self.__first_init:
            chromedriver = "C:/Users/Apply/chromedriver/71-73/chromedriver"
            os.environ["webdriver.chrome.driver"] = chromedriver
            self.d = webdriver.Chrome(chromedriver)  # 模拟打开浏览器
            self.d.maximize_window()  # 窗口最大化

    def find_click(self, locator, times=3, sleep=True):
        '''
            发现元素并且点击
        :param locator:元素
        :param times:超时时间
        :return:
        '''
        if self.wait(locator, times):
            self.d.find_element(*locator).click()
            if sleep:
                time.sleep(1)

    def find_input(self, locator, value, times=3, clean=True):
        '''
            发现元素并且输出值
        :param locator: 元素
        :param value: 输入值
        :param times: 发现超时时间
        :param clean: 是否清空
        :return:
        '''
        if self.wait(locator, times):
            if clean:
                loc = self.d.find_element(*locator)
                loc.send_keys(Keys.CONTROL + 'a')  # 清空原有数据
            self.d.find_element(*locator).send_keys(value)

    def find_list(self, name, text):
        S = Select(self.d.find_element_by_name('cars')).select_by_visible_text('Audi')

    def wait(self, locator, times=3):
        '''
            循环查找元素
            xpath定位("xpath", "//*[@id='form']/span/input[@id='kw']")
        :param locator:("css", "li[class='lgBtns']>a[id='loginSub']")
        :param times:查找多长时间
        :return:
        '''
        try:
            WebDriverWait(self.d, times, 0.2).until(lambda x: x.find_element(*locator))
            return True
        except Exception as err:
            if self.tips:
                print("{}元素不存在：{}".format(str(locator), str(err)))
            return False

    def wait_gone(self, locator, times=3):
        '''
            循环等待元素消失
        :param locator:
        :param times:
        :return:
        '''
        try:
            start_time = time.time()
            while time.time() - start_time < times:
                if not self.wait(locator, 0.5):
                    return True
        except Exception as err:
            if self.tips:
                print(err)

    '''
        self.d.get(path) 打开网址
        self.d.quit() 退出
        self.d.find_element(*locator).click() 点击
        self.d.find_element(*locator).send_keys(value) 输入
        self.d.find_element(*locator).text 获取文本
    '''


if __name__ == "__main__":
    br = Browser()
    br.d.get('http://192.168.3.1/html/index.html')
    if br.wait(('css', "div[class='login_input']>input[id='userpassword']"), times=16):
        br.find_input(('css', "div[class='login_input']>input[id='userpassword']"), "nj12345678", 2)
        br.find_click(('css', "div[id='ember355']>button[id='loginbtn']"), 2)
        br.find_click(('css', "div[class='wrap-icon']>div[class='want_wifi']"), 4)
        br.find_input(('css', "div[class='input_big']>input[id='content_wifi_name2G_ctrl']"), '')
        br.find_input(('css', "div[id='ember568']>input[id='content_wifi_password2G_ctrl']"), '')
        br.find_click(('css', "td>button[id='SsidSettings_submitbutton']"))
        br.wait(('css', "img[src='/res/submit.gif']"), 1)
        br.wait_gone(('css', "img[src='/res/submit.gif']"), 15)
        print('sss')
