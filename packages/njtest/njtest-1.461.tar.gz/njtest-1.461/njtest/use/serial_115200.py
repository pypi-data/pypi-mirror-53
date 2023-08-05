import time
import threading
from njtest.common import nj_file, nj_email
from njtest.serial import nj_serial, serial_count


def keep_data(path, cmd, email=None, prints=False, baudrate=115200):
    '''
        保存打印数据
    :param path: 文件保存目录
    :param cmd:端口号
    :param prints:判断是否打印正连接的端口号
    :return:
    '''
    file_path = "{}/{}在线1.log".format(path, cmd)
    if email == None:
        ser = nj_serial.Ser()
    else:
        ser = nj_serial.Ser(email)
    try:
        ser.connect(port=cmd, baudrate=baudrate, parity='N')
    except Exception as err:
        print("连接端口：" + str(err))
    tips = 0
    while True:
        nj_file.file_add_value(file_path)  # 增加开始打印时间
        time.sleep(5)
        if len(ser.serial_data_115200list) > 0:
            if prints:  # 判断初始为空端口
                if tips < 3:
                    print('新加端口：' + cmd)  # 打印在用端口
                    tips += 1
            nj_file.add_list(file_path, ser.serial_data_115200list)  # 保存数据
            file_path = nj_file.judge_file_size(file_path)  # 判断文件大小
        time.sleep(25)


def print_115200(path, email=None, cmd_list=[], baudrate=115200):
    '''
        115200打印log
    :param path:文件保存目录
    :return:
    '''
    nj_file.path_exists(path)  # 判断文件夹
    ser = nj_serial.Ser()
    if len(cmd_list) > 0:
        print(ser.serial_list)  # 打印当前所有端口
        for cmd in cmd_list:
            threading.Thread(target=keep_data, args=(path, cmd, email, False, baudrate)).start()
    else:
        time.sleep(1)
        print(ser.serial_list)  # 打印当前所有端口
        port_list = ser.check_port()  # 检查可用端口
        if not len(port_list) > 0:
            raise NameError('目前无串口可用,请插入新串口')
        for cmd in port_list:
            threading.Thread(target=keep_data, args=(path, cmd, email, True, baudrate)).start()


def loop_get_data(times=60):
    '''
        循环获取邮件判断
    :param times:获取间隔时间
    :return:
    '''
    while email.printing:
        value = email.get_data()
        if not email.ID == value['Message-ID']:
            for name in email_name_list:
                if name['name'] in value['Subject']:
                    serial_count.on_line(name['name'], name['在线'], name['离线'], excel_path)  # 分析数据
                    email.send_email(value['From'], "{}项目数据结果".format(value['Subject']), content="见附件",
                                     sendfile=[excel_path])
                    email.ID = value['Message-ID']
        time.sleep(times)
    # name = email_name_list[0]
    # serial_count.on_line(name['name'], name['在线'], name['离线'], excel_path)  # 分析数据


if __name__ == '__main__':
    excel_path = './test.xlsx'
    email = nj_email.Email()
    print_115200('马桶', 'congren.yao@broadlink.com.cn', [], 256000)

    # 添加判断内容
    email_name_list = [{'name': '马桶', '在线': 'network status:9', '离线': 'network status:8'},
                       ]
    loop_get_data()
