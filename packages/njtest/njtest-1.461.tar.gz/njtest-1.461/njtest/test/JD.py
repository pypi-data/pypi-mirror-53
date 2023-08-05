import threading
import time
import uiautomator2 as u2
from njtest.common import nj_cmd
from njtest.serial import nj_serial
from njtest.test import System


class JDTest(object):
    __instance = None
    __first_ap_init = False

    def __new__(cls, d):  # 创建类对象时调用
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, d):  # 创建成功调用
        if not self.__first_ap_init:
            self.__first_ap_init = True
            self.d = d
            self.package_name = 'com.jd.smart'
            self.sess = None
            self.one = True

    def ap_init(self, device_name):
        '''
            京东初始化进入到配网界面
        :param device_name:设备名称
        :return:
        '''
        try:
            self.d.app_start(self.package_name)
            self.sess = self.d.session(self.package_name, attach=True)
            self.find_activity()
            self.d(text='测').click(timeout=3)
            self.d(text='开始测试')[0].click(timeout=3)
            self.d(text='添加设备').wait(timeout=10)
            self.d(resourceId='com.jd.smart:id/iv_history').click(timeout=20)
            self.d(resourceId='com.jd.smart:id/iv_history').wait_gone(timeout=60)
            self.d(text='已添加设备').click(timeout=3)
            while not self.d(text=device_name).wait(timeout=1):
                self.d.drag(0.5, 0.2, 0.5, 0.6)
                self.d(resourceId='com.jd.smart:id/pull_to_refresh_gifimage').wait(timeout=2)
                self.d(resourceId='com.jd.smart:id/pull_to_refresh_gifimage').wait_gone(timeout=60)
            self.d(text=device_name).click(timeout=8)
            self.d(text=device_name).wait_gone(timeout=60)
        except Exception as err:
            print("ap_init报错:" + str(err))

    def result_text(self, texts, times):
        '''
            判断是否到继续测试
        :param texts:搜索文字
        :param times:超时时间
        :return:
        '''
        start_time = time.time()
        while True:
            try:
                if texts in self.d(resourceId='com.jd.smart:id/tv_action').get_text(timeout=2):
                    return True
                else:
                    if time.time() - start_time > times:
                        return False
                time.sleep(1)
            except Exception as err:
                print(err)

    def find_wifi(self, wifi_name, wifi_pwd):
        '''
            切换wifi
        :param wifi_name:wifi名称
        :param wifi_pwd:wifi密码
        :return:
        '''
        # self.d.app_stop('com.jd.smart')
        System.find_wifi(self.d, wifi_name, wifi_pwd)  # 切换wifi
        time.sleep(1)
        self.d.app_start('com.jd.smart')  # 回到京东
        time.sleep(1)

    def find_text(self, txt, times=2):
        '''
            查找元素并点击
        :param txt:要查找的文字
        :return:
        '''
        if self.d(text=txt).wait(timeout=times):
            self.d(text=txt).click()

    def find_activity(self):
        '''
            查找Activity判断页面
        :param txt:查找的activity
        :return:
        '''
        try:
            self.d.app_start('com.jd.smart')
            activity = nj_cmd.get_m_activity()
            if not (
                    activity == "com.jd.smart.activity.LoadingActivity" or activity == "com.jd.smart.activity.MainFragmentActivity"):
                self.d.press("back")
                self.find_activity()
        except Exception as err:
            print('find_activity：' + str(err))
            self.find_activity()

    def add_networking(self, wifi_name, wifi_pwd, device_name, ser, cmd='', ap_mode=False, ap_wifi=None,
                       ap_pwd=None, ap_cmd=None):
        '''
            点击+号配网-会先删除设备
        :param wifi_name:wifi名称
        :param wifi_pwd:wifi密码
        :param device_name:设备名称
        :param ser:串口
        :param net_mode:配网模式
        :param cmd:复位指令
        :param ap_mode:ap 模式
        :param ap_wifi:ap wifi名称
        :param ap_pwd:ap wifi密码
        :param ap_cmd:ap 复位指令
        :return:配网是否成功
        '''
        try:
            threading.Thread(target=self.find_text, args=('重新打开应用程序',)).start()
            threading.Thread(target=self.find_text, args=('稍后提醒',)).start()
            if self.sess is None or not self.sess.running():
                if 'com.jd.smart' in nj_cmd.get_m_package():
                    self.d.app_stop(self.package_name)
                self.d.app_start(self.package_name)
                self.sess = self.d.session(self.package_name, attach=True)
            self.find_activity()
            if self.d(text=device_name).wait(timeout=6):  # 发现并删除设备
                self.d(text=device_name).click(timeout=2)
                self.d(resourceId='com.jd.smart:id/web_title').wait(timeout=6)
                self.d(resourceId='com.jd.smart:id/web_title').click(offset=(0.9, 0.5), timeout=3)
                self.d(text='删除设备').wait(timeout=6)
                self.d(text='删除设备').click(timeout=3)
                self.d(text='确定').wait(timeout=6)
                self.d(text='确定').click(timeout=3)
            self.d(resourceId='com.jd.smart:id/iv_right').click(timeout=3)  # 点击+号
            self.d(text='添加设备').wait(timeout=10)
            self.d(resourceId='com.jd.smart:id/iv_history').click(timeout=20)
            self.d(resourceId='com.jd.smart:id/iv_history').wait_gone(timeout=60)
            self.d(text='已添加设备').click(timeout=3)
            while not self.d(text=device_name).wait(timeout=1):
                self.d.drag(0.5, 0.2, 0.5, 0.6)
                self.d(resourceId='com.jd.smart:id/pull_to_refresh_gifimage').wait(timeout=2)
                self.d(resourceId='com.jd.smart:id/pull_to_refresh_gifimage').wait_gone(timeout=60)
            self.d(text=device_name).click(timeout=8)
            self.d(text=device_name).wait_gone(timeout=60)
            self.find_wifi(wifi_name, wifi_pwd)  # 切换wifi
            self.d(resourceId='com.jd.smart:id/tv_pwd').wait(timeout=6)  # 搜索wifi界面
            self.d(resourceId='com.jd.smart:id/tv_pwd').set_text(wifi_pwd)  # 输入wifi密码
            self.d(text='请选择设备要加入的Wi-Fi').click(timeout=2)  # 隐藏输入键盘
            ser.send_cmd(cmd)  # 串口复位
            time.sleep(0.5)
            ser.send_cmd(cmd)  # 串口复位
            self.d(text='下一步').click(timeout=6)
            self.d(resourceId='com.jd.smart:id/id_cb_tip').click(timeout=6)
            time.sleep(1)
            self.d(text='下一步').click(timeout=2)
            self.d(text='添加中').wait(timeout=2)
            if ap_mode:
                if self.d(text="去连接").wait(timeout=35):
                    self.find_wifi(ap_wifi, ap_pwd)  # 切换wifi
                    if self.result_text('完成', 25):
                        return True
                    else:
                        self.find_wifi(wifi_name, wifi_pwd)  # 切回wifi
                else:
                    if self.result_text('完成', 2):
                        return True
                    else:
                        self.find_wifi(wifi_name, wifi_pwd)  # 切回wifi
            if self.result_text('完成', 63):  # 判断是否搜索到设备
                self.d(resourceId='com.jd.smart:id/tv_action').click(timeout=2)
                return True
            else:
                if self.d(text='尝试其他办法').wait(timeout=3):
                    self.d(text='尝试其他办法').click(timeout=2)
                    if self.d(text='提示').wait(timeout=1):
                        self.d(text='确定').click(timeout=2)
                        self.d(text='尝试其他办法').click(timeout=2)
                    self.com_net_ap(wifi_name, wifi_pwd, ap_wifi, ap_pwd, ap_cmd)
                    if self.result_text('完成', 63):  # 判断是否搜索到设备
                        self.d(resourceId='com.jd.smart:id/tv_action').click(timeout=2)
                        return True
                    else:
                        return False
                else:
                    return False
        except Exception as err:
            print('add_networking报错：' + str(err))
            return self.add_networking(wifi_name, wifi_pwd, device_name, ser, cmd, ap_mode, ap_wifi, ap_pwd)

    def com_net_ap(self, wifi_name, wifi_pwd, ap_wifi, ap_pwd, ap_cmd):
        '''
            其他方式中ap配网
        :param wifi_name:wifi名称
        :param wifi_pwd:wifi密码
        :param ap_wifi:ap wifi名称
        :param ap_pwd:ap wifi密码
        :param ap_cmd:ap 复位指令
        :return:
        '''
        self.find_wifi(wifi_name, wifi_pwd)  # 切换wifi
        self.d(resourceId='com.jd.smart:id/tv_pwd').wait(timeout=6)  # 搜索wifi界面
        self.d(resourceId='com.jd.smart:id/tv_pwd').set_text(wifi_pwd)  # 输入wifi密码
        self.d(text='请选择设备要加入的Wi-Fi').click(timeout=2)  # 隐藏输入键盘
        ser.send_cmd(ap_cmd)  # 串口复位
        time.sleep(0.3)
        ser.send_cmd(ap_cmd)  # 串口复位
        self.d(text='下一步').click(timeout=6)
        self.d(resourceId='com.jd.smart:id/id_cb_tip').click(timeout=6)
        time.sleep(1)
        self.d(text='下一步').click(timeout=2)
        self.d(text='添加中').wait(timeout=2)
        if self.d(text="去连接").wait(timeout=36):
            print('去连接ap热点')
            self.find_wifi(ap_wifi, ap_pwd)  # 切换wifi
            if self.result_text('完成', 25):
                return True
            else:
                print('切回wifi')
                self.find_wifi(wifi_name, wifi_pwd)  # 切回wifi
        else:
            if self.result_text('完成', 2):
                return
            else:
                print('切回wifi')
                self.find_wifi(wifi_name, wifi_pwd)  # 切回wifi
                return

    def add_device(self, wifi_name, wifi_pwd, device_name, ser, cmd='a5 a5 5a 5a 98 c1 e8 03 00 00 00 00', ap_mode=False, ap_wifi=None,
                   ap_pwd=None, ap_cmd=None):
        '''
            JD普通+号配网
            ap配网；A5 A5 5A 5A b8 c0 0a 01 00 00 00 00
            一键配网：a5 a5 5a 5a 98 c1 e8 03 00 00 00 00
        :return:
        '''
        sum = 0
        count = 0
        for i in range(100):
            sum += 1
            a = jd.add_networking(wifi_name, wifi_pwd, device_name, ser, cmd, ap_mode, ap_wifi, ap_pwd, ap_cmd)
            if a:
                count += 1
            print(count, sum)


if __name__ == "__main__":
    d1 = u2.connect("")
    jd = JDTest(d1)
    ser = nj_serial.Ser()
    ser.connect(port='COM4', baudrate=9600, parity='N')
    jd.add_device('BL_huawei', 'nj12345678', '公牛智立方USB插座WiFi版新', ser, 'FF 02 02 07 0B FE', False, "JDChaZuo3784", '12345678',
                  'FF 02 02 07 0B FE')
    print('1')
    ser.stop_serial()
    print('通过')
