import os
import re


def get_m_pid(str1):
    i = os.popen('adb shell "ps|grep "'.format(str1))
    return i.read()


# 获取当前activity
def get_m_activity():
    i = os.popen('adb shell dumpsys window | findstr mCurrentFocus')
    a = re.search(r'/(.+)}', i.read())
    if a is not None:
        return a.group(1)
    else:
        return ""


# 获取app包名称
def get_m_package():
    i = os.popen('adb shell dumpsys window | findstr mCurrentFocus')
    a = re.search(r'.+/', i.read())
    if a is not None:
        return a.group()
    else:
        return ""


if __name__ == "__main__":
    print(get_m_pid)
    print(get_m_activity())
