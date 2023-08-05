import time
import threading
from njtest.common import nj_file
from njtest.serial import nj_serial, serial_count
from njtest.utils import nj_parse


def send(sendValue, times=0, path=None, try_cmd=None, send_cmd=None):
    '''
        通过串口发送数据
    :param sendValue:要发送的数据
    :param times:循环发送时间 秒为单位，毫秒0.1
    :param path: 保存log路径 如："./aa.log"
    :param try_cmd: 捕捉結果
    :param send_cmd: 捕捉到后立马发生数据
    :return:
    '''
    ser = nj_serial.Ser()
    print(ser.serial_list)
    ser.connect(port='COM', baudrate=9600, parity='N')  # 连接串口-->此处按协议要求修改
    ser.send_cmd(sendValue, times)  # 发送数据
    # ser.try_data('') 捕捉数据
    if try_cmd is not None:
        threading.Thread(target=ser.try_data,
                         args=(try_cmd, send_cmd, len(ser.serial_data_9600list))).start()  # 线程捕捉结果并发送数据
    if path is not None:
        time.sleep(2)
        nj_file.add_list(path, ser.serial_data_9600list)  # 保存日志结果


if __name__ == '__main__':
    cmd = 'BB 01 00 06 0B 01 00 00 00 00 00 00 00 00 00 08'  # 初始数据
    cmd = nj_parse.data_replace_byt(cmd, {2: [0, 1]})  # 修改数据
    print(cmd)
    sendValue = nj_parse.checksum(cmd, formula='CRC', position=5)  # 为数据增加效验位
    print(sendValue)
    # send(sendValue)  # 发送数据
    # print(nj_parse.hex_to_byt(cmd, 4)) # 查看串口数据位
    serial_count.cont_9600()
