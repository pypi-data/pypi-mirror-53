import os
import re
import threading


class Logcat(threading.Thread):
    
    def __init__(self, ui2, logPath):
        '''
        :param u3:USB对象u2.connect_usb()
        :param logPath:日志保存目录
        '''
        super(Logcat, self).__init__()
        self.ui2 = ui2
        self.logPath = logPath
    
    def run(self):
        self.ui2.adb_shell('logcat -c')
        os.system('adb logcat *:D > %s' % self.logPath)
    
    def stop(self, keyword='SyS_rt_sigsuspend'):
        str = self.ui2.adb_shell('ps | grep %s' % keyword).split('shell')[1].strip()  # ps | grep '系统打印关键字'
        self.ui2.adb_shell('logcat -c && kill %s' % re.split('\s+', str)[0])
