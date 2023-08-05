# pip install opencv-python
# pip install --pre -U uiautomator2
# pip install --pre --upgrade weditor
# adb shell dumpsys window | findstr mCurrentFocus  获取包名
# python -m uiautomator2 init 初始化设备
# python -m weditor 获取视图

import uiautomator2 as u2


class connect(object):
    __instance = None
    __first_init = False

    def __new__(cls, ip=''):  # 创建类对象时调用
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, ip=''):  # 创建成功调用
        if not self.__first_init:
            self.__first_init = True
            self.u = u2.connect_usb()
            self.d = u2.connect(ip)

    '''
        ui2接口
        安卓app：d.app_install('http://some-domain.com/some.apk')
        启动app：d.app_start(package_name)
        停止app：d.app_stop('com.example.hello_world')
        保持登录启动：sess = d.session(package_name,attach = True)
        检验app是否闪退：sess.running()
        等待查找：d().wait()   和exists
        等待元素离去：d().wait_gone()
        点击：d().click()
        双击：d.double_click(x,y)
        长按：d.long_click(x,y)
        滑动：d.swipe(x1,y1,x2,y2)
        拖动：d.drag(x1,y1,x2,y2)
        手机截屏：self.d.screenshot(path)
        判断元素是否可点击：d(test='aaa').info['clickable']
        
        获取文本：d(test='aaa').get_text()
        设置文本：d(test='aaa').set_text()
        获取元素中心点：x,y = d(text='Settings').center()
        获取tost：d.toast.get_message(5.0, 1 ,'默认消息')
        
        获取屏幕状态：d.info.get('screenOn')
        打开屏幕：d.screen_on()
        关闭屏幕：d.screen_off()
        
        系统按钮：d.press(key)
        # key == "back"):  # 返回键
        # key == "menu"):  # 按菜单键
        # key == "home"):  # 返回主页
        # key == "power"):  # 按power键
        # key == "recent"):  # 按杀进程键
        # key == "volume_up"):  # 按音量上键
        # key == "volume_down"):  # 按音量下键
        # key == "enter"):  # 按enter键
    '''
