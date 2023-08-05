from njtest.common import nj_file, nj_excel
from njtest.utils import nj_re, nj_time

sheet = '在线统计'
excel_path = './test.xlsx'
excel = nj_excel.Excel(excel_path, True)


def analysis(list1, list2, initdata=None, enddata=None):
    '''
        分析日志+结果记录
    :param list1:在线列表
    :param list2:离线列表
    :param initdata:第一行
    :param enddata:最后一行
    :return:
    '''
    ci = 0
    end_time = 0
    end_j = 0
    time_list = []
    excel.set_col_width(excel_path, sheet, [12, 12, 12])
    ws = excel.get_sheet(excel_path, sheet)
    if initdata is None or enddata is None:
        ws['A1'] = '{}-->{}'.format("", "")
    else:
        ws['A1'] = '{}-->{}'.format(nj_time.get_time(initdata), nj_time.get_time(enddata))
    ws.append(['重连耗时(S)', '离线时间', '在线时间'])
    excel.set_row_colour(excel.wb, ws, 2)
    for i in range(len(list2)):
        if end_time == 0 or float(nj_time.count_time(end_time, list2[i])) > 0:  # 离线时间大于最后结束时间
            off = True
            for j in range(end_j, len(list1)):
                times = float(nj_time.count_time(list2[i], list1[j]))
                if times > 0:  # if在线大于离线
                    ci += 1
                    end_time = list1[j]
                    ws.append([times, nj_time.get_time(list2[i]), nj_time.get_time(list1[j])])  # 将离线数据添加到excel
                    time_list.append(times)
                    off = False
                    end_j = j
                    break
            if off:
                ci += 1
                ws.append(["最后一次离线时间：{}".format(nj_time.get_time(list2[i]))])
                break
    if len(time_list) > 0:
        if initdata is None or enddata is None:
            ws['A1'] = '共配网{}次，最大配网时间:{}秒，平均配网时间:{}秒'.format(ci, "%.3f" % float(max(time_list)),
                                                             "%.3f" % float(sum(time_list) / len(time_list)))
        else:
            ws['A1'] = '共离线{}次，总时间：{}秒，总离线:{}秒，最大离线:{}秒，平均离线:{}秒,时间：{}-->{}'.format(ci, nj_time.count_time(initdata,
                                                                                                           enddata),
                                                                                    "%.3f" % float(sum(time_list)),
                                                                                    "%.3f" % float(max(time_list)),
                                                                                    "%.3f" % float(sum(time_list) / len(
                                                                                        time_list)),
                                                                                    nj_time.get_time(initdata),
                                                                                    nj_time.get_time(enddata))
    else:
        ws['A1'] = '共离线{}次，总时间：{}秒，时间：{}-->{}'.format(ci, nj_time.count_time(initdata, enddata),
                                                      nj_time.get_time(initdata), nj_time.get_time(enddata))
    ws.merge_cells('A1:C1')  # 合并单元格
    excel.end_save(excel_path, sheet)


def on_line(path, key1, key2, excel_path1='./test.xlsx'):
    global sheet, excel_path, excel
    '''
        115200数据判断在线离线
    :param path:文件目录
    :param key1:在线关键字
    :param key2:离线关键字
    :param excel_path:excel保存路径
    :return:离线结果
    '''
    aa = []
    excel_path = excel_path1
    excel = nj_excel.Excel(excel_path1, True)  # 创建Excel
    file_name = nj_file.get_son_file_info(path)  # 获取目录下所有子文件
    for i in range(len(file_name)):
        if i == 0:
            aa.append("{}".format(nj_re.find_data(file_name[i], 'COM\d+'), i))
        else:
            if not "{}".format(nj_re.find_data(file_name[i], 'COM\d+')) in aa:
                aa.append(nj_re.find_data(file_name[i], 'COM\d+'))
    for i in range(len(aa)):  # 遍历当前所有文件
        list1 = []
        list2 = []
        initdata = None  # 包含初始时间数据
        enddata = None  # 包含结束时间数据
        sheet = aa[i]  # 将sheet指向当前端口
        for name in file_name:
            if nj_re.find_data(name, 'COM\d+') == aa[i]:
                list1.extend(nj_file.read_file("{}/{}".format(path, name), key1))
                list2.extend(nj_file.read_file("{}/{}".format(path, name), key2))
                if initdata is None:
                    initdata = nj_file.read_file_count("{}/{}".format(path, name))[0]
                enddata = nj_file.read_file_count("{}/{}".format(path, name))[1]
        analysis(list1, list2, initdata, enddata)


def cont_9600(try_cmd, serial_data_9600list):
    '''
        9600数据分析
    :param try_cmd:查询的数据
    :param serial_data_9600list:日志list
    :return:
    '''
    max = len(serial_data_9600list)
    for i in range(max - 1):
        listdata = "{}{}".format(nj_re.find_rm_second(serial_data_9600list[i]),
                                 nj_re.find_rm_second(serial_data_9600list[i + 1]))  # 去除时间的两组数据合并
        if nj_re.rm_to_str(try_cmd, filter=' ') in nj_re.rm_to_str(listdata, filter=' '):  # 去空格后数据对比
            return i
        elif i == (max - 2):
            return 0
