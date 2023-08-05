import os
import sys
import shutil


# python setup.py bdist --format=wininst  生成exe文件
# pyinstaller -F hello.py 生成exe文件

# python setup.py sdist 打包成zip文件发布
# twine upload dist/njtest-1.461.tar.gz 上传到pypi服务器
# pip install --pre --upgrade njtest 更新本地环境

class ManagementUtility:

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.cwd = os.getcwd()  # 获取当前工作路径
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.settings_exception = None

    def start(self):
        name = None
        if self.argv[2] == "9600":
            name = "serial_9600.py"
        if self.argv[2] == "115200":
            name = "serial_115200.py"
        if name is None:
            name = str(self.argv[2]) + '.py'
        try:
            oldname = self.path + "\\use\\{}".format(name)
            newname = self.cwd + "\\{}".format(name)
            shutil.copyfile(oldname, newname)  # 复制代码
        except Exception as err:
            print(err)

    def execute(self):
        if self.argv[1] == 'start':
            self.start()
        tips = '''  
        njtest start 9600-->生成串口9600打印类
        njtest start 115200-->生成串口115200打印类
        njtest start xxx-->查找名字生成
        '''
        if self.argv[1] == 'help':
            print(tips)


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
