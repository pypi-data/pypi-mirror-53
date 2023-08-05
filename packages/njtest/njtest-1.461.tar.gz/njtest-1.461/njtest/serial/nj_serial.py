import time
import serial
import random
import datetime
import threading
import serial.tools.list_ports
from njtest.common import nj_file, nj_email
from njtest.utils import nj_parse, nj_re, nj_time

'''
    串口通讯模块
'''


class Ser(object):

    def __init__(self, email_name=None):
        self.start_time = time.time()  # 初始9600记录时间
        self.serial_data = []  # 9600字节存储数据列表
        self.serial_data_9600list = []  # 9600列表存储数据列表
        self.serial_data_115200list = []  # 115200列表存储数据列表
        self.state = True  # 判断serial是否打印数据
        self.serial_list = self.get_port()  # 获取所有的COM端口
        self.content = ""
        self.email_sum = 366
        self.email_name = email_name
        self.tips = 2
        if email_name is not None:
            self.email = nj_email.Email()

    def connect(self, port='COM', baudrate=115200, parity='N', bytesize=8, stopbits=1):
        '''
            连接串口
        :param port:端口号
        :param baudrate:波特率(普通模块:9600,115200，5981:256000)
        :param parity:效验位('N', 'E', 'O', 'M', 'S')
        :param bytesize:数据位
        :param stopbits:停止位
        :return:
        '''
        if port == 'COM':
            try:
                self.ser = serial.Serial(port=self.serial_list[0], baudrate=baudrate, parity=parity, bytesize=bytesize,
                                         stopbits=stopbits, timeout=60)
            except Exception as err:
                raise NameError("串口未连接或被占用：" + str(err))
        else:
            try:
                self.ser = serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize, stopbits=stopbits, timeout=60)
            except Exception as err:
                raise NameError("串口未连接或被占用：" + str(err))
        if self.ser.isOpen():  # 判断串口是否连接
            self.thread_read = threading.Thread(target=self.start_read_cmd, args=())
            self.thread_read.start()
            if self.ser.baudrate == 9600:
                self.thread_read_9600 = threading.Thread(target=self.start_9600, args=())
                self.thread_read_9600.start()
        else:
            raise NameError('串口未连接,请重试')

    def check_port(self):
        '''
            打印可用端口
        :return:返回可用端口列表
        '''
        list1 = []
        for i in self.serial_list:
            try:
                ser = serial.Serial(port=i)
                ser.close()
                list1.append(i)
            except Exception as err:
                pass
        return list1

    def send_cmd(self, cmd, times=0):
        '''
            发送数据
        :param cmd:要发送的数据
        :param times:循环发送数据时间
        :return:
        '''
        self.ser.write(nj_parse.str_to_hexstr(cmd))
        self.serial_data_9600list.append(self.add_time(cmd, "发送："))
        while times != 0 and self.state:
            time.sleep(times)
            self.ser.write(nj_parse.str_to_hexstr(cmd))
            self.serial_data_9600list.append(self.add_time(cmd, "发送："))
            print(self.add_time(cmd, "发送："))

    def start_read_cmd(self):
        '''
            开启读取串口数据
        :return:
        '''
        while self.state and self.state:
            try:
                if self.ser.isOpen():
                    if self.ser.baudrate != 9600:
                        data = self.ser.readline()
                        if data != b'':
                            content = nj_parse.bytes_to_str(data, encoding="utf-8")
                            datas = content.replace('\n', '').replace('\r', '')  # 去除换行
                            self.serial_data_115200list.append(self.add_time(datas))  # 添加115200打印数据
                    else:
                        data = self.ser.read()
                        self.serial_data.append(data)
                        self.start_time = time.time()
                        # print(nj_parse.bytes_to_hexstr(data)) # 查看9600单个数据
                    if self.tips > 0:
                        self.tips -= 1
                        print("{} ：{}".format(self.ser.port, self.add_time(data)))  # 刚启动时打印数据
            except Exception as err:
                print("读取串口数据报错" + str(err))
                if self.email_sum > 0:
                    self.email_sum -= 1
                elif self.email_sum == 0:
                    if self.email_name is not None:
                        self.email.send_email(self.email_name, "串口松动了", "读取串口数据报错:" + str(err))
                        self.email_sum -= 1  # 保证只发送一次邮件

    def start_9600(self):
        '''
            启动9600循环打印
        :return:
        '''
        while self.state:
            if (time.time() - self.start_time) >= 0.06 and len(self.serial_data) > 4:
                self.content = nj_parse.list_bytes_to_hexstr(self.serial_data)
                self.serial_data = []
                self.start_time = time.time()
                self.serial_data_9600list.append(self.add_time(self.content))
                # print("结果：" + self.add_time(self.content))

    def try_data(self, try_cmd, send_cmd=None, amin=1, times=10):
        '''
            循环捕捉-->发送数据
        :param try_cmd:要捕捉的数据
        :param send_cmd:捕获后发送数据
        :param amin:捕捉数据的起始位置
        :param times:等待时间
        :return:捕捉结果
        '''
        start_time = time.time()
        while self.state:
            if time.time() - start_time < times:
                amax = len(self.serial_data_9600list)
                for i in range(amin - 1, amax):
                    if i < len(self.serial_data_9600list) - 1:
                        listdata = "{}{}".format(nj_re.find_rm_second(self.serial_data_9600list[i]),
                                                 nj_re.find_rm_second(self.serial_data_9600list[i + 1]))  # 去除时间的两组数据合并
                        if nj_re.rm_to_str(try_cmd, filter=' ') in nj_re.rm_to_str(listdata, filter=' '):  # 去空格后数据对比
                            if send_cmd is not None:
                                self.send_cmd(send_cmd)
                                self.serial_data_9600list.append(self.add_time(send_cmd, "发送："))
                                return True
                            else:
                                return i
                amin = amax
            else:
                # print("未捕捉到")
                return False

    def stop_serial(self):
        '''
            关闭串口连接
        :return:
        '''
        self.state = False
        self.ser.close()

    def add_time(self, data, value=''):
        '''
            为数据增加时间节点
        :param data:初始数据
        :param value:中间要插入的数据
        :return:合并后数据
        '''
        return "{} {}{}".format(nj_time.get_time(), value, data)

    def get_port(self):
        '''
            获取所有串口号
        :return: 所有串口的名字-->如‘com3’
        '''
        all_serial_list = self.show_all_serial()
        usb_serial_list = []
        for i in all_serial_list:
            if 'USB Serial Port' in i[1]:
                usb_serial_list.append(i[0])
        return usb_serial_list

    def show_all_serial(self):
        '''
            获取所有的串口信息
        :return:所有的串口及每个窜口的信息
        '''
        plist = list(serial.tools.list_ports.comports())  # 获取串口信息
        all_serial_list = []
        for p in plist:
            serial_info = []
            for i in p:
                serial_info.append(i)
            all_serial_list.append(tuple(serial_info))
        return all_serial_list


if __name__ == '__main__':
    ser = Ser()  # 打印所有串口号
    print(ser.serial_list)
    ser.connect(baudrate=9600, parity='E')
    ser.serial_state = True
    time.sleep(0.5)
    # cmd = 'BB 01 00 06 0B 03 00 00 00 00 00 00 00 00 00 08 BC'
    cmd = 'BB 01 00 06 0B {} 00 00 00 00 00 00 00 00 00 08'.format(nj_parse.byt_to_hex([1, 2]))
    result = 'BB 00 01 06 09 00 00 00 00 00 00 00 00 80 35 FC'
    a = 0
    # print(nj_parse.data_replace_byt(result, {1: [1, 2], 2: [1, 2]})) # 更换发送数据
    for i in range(1, 5):
        sendValue = nj_parse.checksum(cmd, formula='BCC')
        print(sendValue)
        # ser.send_cmd(sendValue)
    #     if ser.try_data(result, amin=len(ser.serial_data_9600list)):  # 捕捉結果
    #         a += 1
    #     print(i, a)
    #     time.sleep(random.uniform(5, 10))
    #     nj_file.add_list("./aa.log", ser.serial_data_9600list)  # 将数据写入到文件
    # print(ser.serial_data_9600list)
    # print(ser.serial_data_115200list)
