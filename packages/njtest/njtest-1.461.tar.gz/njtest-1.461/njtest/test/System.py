import time
import uiautomator2 as u2
from njtest.common import nj_cmd
from njtest.ui2 import browser
from selenium.webdriver.common.action_chains import ActionChains


def find_wifi(d, wifi_name, wifi_pwd):
    '''
        查找wifi切换
    :param wifi_name:wifi名称
    :param wifi_pwd:wifi密码
    :return:
    '''
    try:
        d.app_start('com.example.aux1')
        if nj_cmd.get_m_activity() == 'com.android.settings.wifi.WifiPickerActivity':  # 判断当前是否在wifi界面
            d.press("back")
        print(d(resourceId='com.example.aux1:id/wifi_name_tv').get_text(timeout=3))
        if not d(resourceId='com.example.aux1:id/wifi_name_tv').get_text(timeout=3) == wifi_name:
            d(resourceId='com.example.aux1:id/wifi_iv').click(timeout=3)
            locator = d(resourceId='android:id/title')
            d.swipe(0.5, 0.1, 0.5, 0.6, 0.5)
            if d(resourceId='com.android.settings:id/scanning_progress').wait(timeout=5):
                d(resourceId='com.android.settings:id/scanning_progress').wait_gone(timeout=20)
            try:
                if locator.wait(timeout=10):
                    time.sleep(0.3)
                    for zhi in range(6):
                        i = len(locator)
                        for view in locator:
                            get_value = view.get_text(timeout=6)
                            # print(get_value)
                            if get_value == wifi_name:
                                view.click(timeout=3)
                                if d(text='忘记').wait(timeout=2):
                                    d(text='取消').click(timeout=3)
                                if d(text='连接').wait(timeout=2):
                                    if d(resourceId='com.android.settings:id/password').wait(timeout=1):
                                        d(resourceId='com.android.settings:id/password').set_text(wifi_pwd)
                                    d(text='连接').click(timeout=3)
                                if d(resourceId='com.android.settings:id/scanning_progress').wait(timeout=1):
                                    d(resourceId='com.android.settings:id/scanning_progress').wait_gone(timeout=6)
                                find_wifi(d, wifi_name, wifi_pwd)  # 再次确定wifi名称
                                return True
                        x, y = locator[i - 2].center()
                        x1, y1 = locator[0].center()
                        d.swipe(x, y, x1, y1, 1)
                    find_wifi(d, wifi_name, wifi_pwd)  # 再次确定wifi名称
            except Exception as err:
                print('系统wifi界面报错：' + str(err))
                find_wifi(d, wifi_name, wifi_pwd)
    except Exception as err:
        print('切换wifi报错：' + str(err))


def name_password(username, password):
    '''
        更换路由名称和密码
    :param username:路由名称
    :param password:路由密码
    :return:
    '''
    br.d.get('http://192.168.3.1/html/index.html')
    if br.wait(('css', "div[class='login_input']>input[id='userpassword']"), times=16):
        br.find_input(('css', "div[class='login_input']>input[id='userpassword']"), "nj12345678", 2)  # 登录输入密码
        br.find_click(('css', "div[id='ember355']>button[id='loginbtn']"), 2, False)  # 登录
        br.wait_gone(('css', "div[id='ember355']>button[id='loginbtn']"), 8)  # 等待登录跳转
        br.find_click(('css', "div[class='wrap-icon']>div[class='want_wifi']"), 2)  # 点击WiFi按钮
        br.find_input(('css', "div[class='input_big']>input[id='content_wifi_name2G_ctrl']"), username)  # 修改WiFi名
        br.find_input(('css', "div[id='ember568']>input[id='content_wifi_password2G_ctrl']"), password)  # 修改wifi密码
        br.find_click(('css', "td>button[id='SsidSettings_submitbutton']"))  # 点击确定
        br.wait(('css', "img[src='/res/submit.gif']"), 1)  # 发现loading
        br.wait_gone(('css', "img[src='/res/submit.gif']"), 15)  # 等待loading取消


def model(model_name, password=None):
    '''
        切换wifi模式
    :param model_name:模式名称：不加密- WPA2 PSK 模式- WPA/WPA2 PSK 混合模式
    :param password:wifi密码
    :return:
    '''
    br.d.get('http://192.168.3.1/html/index.html')
    if br.wait(('css', "div[class='login_input']>input[id='userpassword']"), times=16):
        br.find_input(('css', "div[class='login_input']>input[id='userpassword']"), "nj12345678", 2)  # 登录输入密码
        br.find_click(('css', "div[id='ember355']>button[id='loginbtn']"), 2, False)  # 登录
        br.wait_gone(('css', "div[id='ember355']>button[id='loginbtn']"), 8)  # 等待登录跳转
        br.find_click(('css', "div[class='wrap-icon']>div[class='want_wifi']"), 2)  # 点击WiFi按钮
        br.find_click(('css', "div[class='wrap-icon']>font[text='WPA2 PSK模式']"), 2)  # 点击模式按钮
        br.find_click(('css', "div[class='bigselect wordbreak']"), 2)  # 点击模式按钮
        if model_name == '不加密':
            br.find_click(('css', "div[id='None_BigSelectBoxItemID']"), 2)  # 点击模式弹出框内容
        if model_name == 'WPA2 PSK 模式':
            br.find_click(('css', "div[id='wifi_secopt2G_ctrl_selectlist_childselect']"), 2)
        if model_name == 'WPA/WPA2 PSK 混合模式':
            br.find_click(('css', "div[id='WPAand11i_BigSelectBoxItemID']"), 2)
        if password is not None:
            br.find_input(('css', "div[id='ember568']>input[id='content_wifi_password2G_ctrl']"), password)  # 修改wifi密码
        br.find_click(('css', "td>button[id='SsidSettings_submitbutton']"))  # 点击确定
        br.wait(('css', "img[src='/res/submit.gif']"), 1)  # 发现loading
        br.wait_gone(('css', "img[src='/res/submit.gif']"), 15)  # 等待loading取消


def wifi_set():
    br.d.get('http://192.168.3.1/html/index.html')
    if br.wait(('css', "div[class='login_input']>input[id='userpassword']"), times=16):
        br.find_input(('css', "div[class='login_input']>input[id='userpassword']"), "nj12345678", 2)  # 登录输入密码
        br.find_click(('css', "div[id='ember355']>button[id='loginbtn']"), 2, False)  # 登录
        br.wait_gone(('css', "div[id='ember355']>button[id='loginbtn']"), 8)  # 等待登录跳转
        br.find_click(('css', "div[class='wrap-icon']>div[class='want_more']"), 2)  # 点击WiFi按钮
        br.find_click(('css', "div[class='paddingleft-20']"), 2)  # 点击WiFi按钮
        br.d.find_elements_by_class_name("paddingleft-20")[3].click()  # wifi设置按钮
        br.find_click(('css', "div[id='wifi_channel24g_ctrl_selectlist_childselect']"))  # 点击信道
        move_element = br.d.find_element_by_id("0_BigSelectBoxScrollItemID")
        ActionChains(br.d).move_to_element(move_element).perform()
        js = "scrollTo(100,450);"
        # js = "window.scrollTo(100,450);"
        br.d.execute_script(js)
        # br.find_click(('css', "div[id='13_BigSelectBoxScrollItemID']"))  # 13信道


if __name__ == "__main__":
    # d1 = u2.connect("")
    # while True:
    #     print('换网---BL_huawei')
    #     find_wifi(d1, 'BL_huawei', 'nj12345678')
    #     print('换网---mdww')
    #     find_wifi(d1, 'mdww', 'nj12345678')
    # 游览器模拟运行
    br = browser.Browser()
    wifi_set()
    # model('不加密', 'nj12345678')
    # name_password('BL_huawei', 'nj12345678')
