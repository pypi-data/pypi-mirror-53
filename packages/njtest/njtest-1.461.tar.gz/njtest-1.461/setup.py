from setuptools import setup

setup(
    name="njtest",  # 这里是pip项目发布的名称
    version="1.461",  # 版本号，数值大的会优先被pip
    keywords=("pip", "SICA", "featureextraction"),
    description="Automated Packaging Tool",  # 平台提示
    long_description="Automated Packaging Tool",
    license="MIT Licence",

    url="https://github.com/congrenya/njtest/blob/master/njtest.py",  # 项目相关文件地址，一般是github
    author="Stephen Yao",
    author_email="a1123547734@163.com",

    packages=['njtest', 'njtest.common', 'njtest.utils', 'njtest.use', 'njtest.serial', 'njtest.ui2', 'njtest.test'],
    # 打包文件夹
    include_package_data=True,  # 自动打包文件夹内所有数据
    zip_safe=True,  # 设定项目包为安全，不用每次都检测其安全性
    entry_points={'console_scripts': [
        'njtest = njtest.hello:execute_from_command_line',
    ]},  # 在windows下Python目录的scripts下生成exe文件
    platforms="any",
    install_requires=['numpy', 'pyserial', 'openpyxl', 'pillow', 'uiautomator2', 'Appium-Python-Client']  # 这个项目需要的第三方库
)
