import threading
import time
import uiautomator2 as u2
from njtest.common import nj_excel, nj_file
from njtest.utils import nj_time

'''
    京东插座断电重启
    用于模块断电，断网，断外网
'''


def analysis(path, key):
    '''
        分析日志
    :param path:目录
    :param key: 查找的文字
    :return:
    '''
    file_name = nj_file.get_son_file_info(path)  # 获取目录下所有子文件
    print(file_name)
    for name in file_name:
        print(name)
        list1 = []
        list1.extend(nj_file.read_file("{}/{}".format(path, name), key))
        excel = nj_excel.Excel(excel_path)
        ws = excel.wb[excel_sheet]
        rows = ws.rows
        excel.set_col_width(excel_path, name, [12, 12, 12])
        ws = excel.get_sheet(excel_path, name)
        ws.append(['重连时间(S)', '电源开时间', '连上云时间'])
        end = 0
        if len(list1) < 1:
            ws.append(['连云全部失败'])
            excel.end_save(excel_path, name)
            continue
        for row in rows:
            line = [col.value for col in row]
            if line[0] == '开':
                if float(nj_time.count_time(line[1], list1[len(list1) - 1])) < 0:  # 判断excel时间是否大于最大连云时间
                    ws.append(['重连一直失败', line[1], list1[len(list1) - 1]])
                    break
                for i in range(end, len(list1)):
                    times = float(nj_time.count_time(line[1], list1[i]))
                    if times > 0:
                        # print(list1[i])
                        end = i
                        if times < 60:
                            ws.append([times, line[1], nj_time.get_time(list1[i])])
                        else:
                            ws.append(['重连大于60S', line[1], nj_time.get_time(list1[i])])
                        break
        excel.end_save(excel_path, name)


def find_text(txt, times=2):
    '''
        查找元素并点击
    :param txt:要查找的文字
    :return:
    '''
    if d(text=txt).wait(timeout=times):
        d(text=txt).click()


def switch(control='开'):
    '''
        控制插座开关
    :param control:开或关
    :return:
    '''
    global sess, d, excel
    if sess is None or sess.running() is False:
        d.app_start(package_name)
        sess = d.session(package_name, attach=True)
    threading.Thread(target=find_text, args=('稍后提醒',)).start()
    d(text='设备').wait(timeout=60)
    if control == '开':
        if d(text='电源关').wait(timeout=2):
            d(resourceId="com.jd.smart:id/device_power").click(timeout=2)
            d(resourceId='com.jd.smart:id/pb_card_status').wait(timeout=3)
            d(resourceId='com.jd.smart:id/pb_card_status').wait_gone(timeout=30)
        if d(text='电源开').wait(timeout=3):
            print('{} {}'.format(nj_time.get_time(), control))
            excel.add_value(excel_path, '插座断电记录', [control, nj_time.get_time()])
            return
        else:
            switch('开')
    if control == '关':
        if d(text='电源开').wait(timeout=2):
            d(resourceId="com.jd.smart:id/device_power").click(timeout=2)
            d(resourceId='com.jd.smart:id/pb_card_status').wait(timeout=3)
            d(resourceId='com.jd.smart:id/pb_card_status').wait_gone(timeout=30)
        if d(text='电源关').wait(timeout=3):
            print('{} {}'.format(nj_time.get_time(), control))
            excel.add_value(excel_path, '插座断电记录', [control, nj_time.get_time()])
            return
        else:
            switch('关')


def power():
    '''
        插座控制
    :return:
    '''
    global excel, sess, d
    d = u2.connect("")
    d.app_start(package_name)
    sess = d.session(package_name, attach=True)
    excel = nj_excel.Excel(excel_path, True)  # 创建Excel
    excel.add_value(excel_path, excel_sheet, ['操作', '时间'])
    excel.set_col_width(excel_path, excel_sheet, [5, 12])
    for i in range(30):
        switch('关')
        time.sleep(60 * 20)
        switch('开')
        time.sleep(60 * 10)
    excel.end_save(excel_path, excel_sheet)


if __name__ == "__main__":
    package_name = 'com.jd.smart'
    excel_path = './插座断电.xlsx'
    excel_sheet = '插座断电记录'
    power()
    '''
        分析日志
        1、创建美的文件夹
        2、将所以日志放到此文件内
        3、将power()注释
        4、将analysis取消注释，运行
    '''
    # analysis('美的', 'network status:9')
