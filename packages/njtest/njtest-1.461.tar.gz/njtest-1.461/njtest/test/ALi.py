import uiautomator2 as u2
from njtest.serial import nj_serial
from njtest.utils import nj_time


class ALiTest(object):
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
            self.package_name = 'com.alibaba.ailabs.tg'
            self.toast = ''
            self.state = False
            self.one = True
            self.sess = None

    def init(self):
        self.d.app_stop(self.package_name)  # 停止App运行
        self.d.app_start(self.package_name)  # 重新启动App运行
        self.sess = self.d.session(self.package_name, attach=True)
        self.d(text='扫一扫').wait(timeout=60)

    def add_device(self, cmd):
        if self.sess is None or self.sess.running() is False:
            self.init()
        self.find()
        self.d(text='扫一扫').click(timeout=2)
        self.d(resourceId='com.alibaba.ailabs.tg:id/ar_nav_bar_album').click(timeout=2)
        self.d(text='相册').click(timeout=6)
        self.d(className='com.sec.samsung.gallery.glview.composeView.ThumbObject')[0].click(timeout=6)
        self.d(className='com.sec.samsung.gallery.glview.composeView.ThumbObject')[0].click(timeout=6)
        self.d(text='完成').click(timeout=6)
        self.d(description='输入 Wi-Fi 密码').wait(timeout=60)
        self.d.xpath(
            '//*[@resource-id="com.alibaba.ailabs.tg:id/weex_render_view"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]').set_text(
            'nj12345678')
        # self.d.set_fastinput_ime(True)
        # self.d.clear_text()
        # self.d.send_keys("nj12345678")
        # time.sleep(0.5)
        # self.d.set_fastinput_ime(False)
        self.d(description='下一步').click(timeout=2)
        ser.send_cmd(cmd)  # 串口复位
        self.d.xpath(
            '//*[@resource-id="com.alibaba.ailabs.tg:id/weex_render_view"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.ImageView[1]').click()
        self.d(description='我确定，下一步').click(timeout=6)
        return self.netwd_result()

    def netwd_result(self):
        '''
            联网结果返回
        :return:
        '''
        while True:
            if self.d(description='智能设备配对成功').wait(timeout=6):
                return True
            elif self.d(description='智能设备配对失败').wait(timeout=6):
                return False

    def find(self):
        '''
            发现是否到初始界面
        :return:
        '''
        while not self.d(text='扫一扫').wait(timeout=0.6):
            self.d.press("back")


if __name__ == "__main__":
    d1 = u2.connect("")
    ali = ALiTest(d1)
    ser = nj_serial.Ser()
    ser.connect(port='COM4', baudrate=9600, parity='N')
    sum = 0
    second = 0
    for i in range(100):
        sum += 1
        print(nj_time.get_time())
        if ali.add_device('bb 02 00 00 00 00 00 00 00 00 00 00 b8 0b 55'):
            second += 1
        print(second, sum)
    # ali.add_device('BL_huawei', 'nj12345678', '希箭智能马桶', ser, False, 'a5 a5 5a 5a 98 c1 e8 03 00 00 00 00')
    # print('1')
    # ser.stop_serial()
    # print('通过')
