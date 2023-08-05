import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from njtest.common import nj_file


class Email(object):

    def __init__(self, user='485068513@qq.com', pop_password='ahutxgmyrnbwbhca', smtp_password='ctohqkzoqmombjij'):
        self.user = user
        self.password = pop_password
        self.pop3_server = 'pop.qq.com'
        self.smtpserver = 'smtp.qq.com'  # 登录相关信息
        self.sender = user
        self.smtp_password = smtp_password
        self.ID = self.get_data()['Message-ID']
        self.printing = True  # 判断是否循环获取邮件

    def send_email(self, receiver, subject, content, sendfile=[]):
        '''
            发送邮件
        :param receiver:接收的邮箱号
        :param subject:邮件主题
        :param content:邮件内容
        :param sendfile:附件地址列表
        :return:
        '''
        try:
            self.smtp = smtplib.SMTP()  # 创建SMTP实例
            self.smtp.connect(self.smtpserver)  # 连接服务器
            self.smtp.login(self.user, self.smtp_password)  # 登录邮箱
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = subject
            msgRoot['From'] = Header(self.user)
            msgRoot['To'] = receiver
            msgtext = MIMEText(content, _subtype='plain', _charset='utf-8')  # subtype有plain,html等格式，避免使用错误
            msgRoot.attach(msgtext)
            for filepath in sendfile:
                att = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')  # 创建带附件的实例
                att["Content-Type"] = 'application/octet-stream'
                att.add_header('Content-Disposition', 'attachment', filename=(
                    'gbk', '',
                    '{}{}.xlsx'.format(nj_file.get_file_name(filepath)[0], '在线情况')))  # 设置邮件显示的文件名称,filename可随便改
                encoders.encode_base64(att)
                msgRoot.attach(att)
            self.smtp.sendmail(self.sender, receiver, msgRoot.as_string())  # 发送邮件
            self.smtp.quit()
            self.smtp.close()
            print("发送成功")
        except smtplib.SMTPException as sm:
            print("发送邮箱出错：" + str(sm))

    def loop_get_data(self, times=60):
        '''
            循环获取邮件
        :param times:获取间隔时间
        :return:
        '''
        while self.printing:
            value = self.get_data()
            if not self.ID == value['Message-ID']:
                # self.send_email(value['From'], "{}项目数据结果".format(value['Subject']), content="见附件")
                self.ID = value['Message-ID']
            time.sleep(times)

    def get_data(self):
        '''
            获取最新一封邮件, 注意索引号从1开始:
        :return:
        '''
        try:
            self.server = poplib.POP3_SSL(self.pop3_server)  # 连接到POP3服务器
            self.server.user(self.user)  # 身份认证
            self.server.pass_(self.password)
            self.resp, self.mails, self.octets = self.server.list()
            index = len(self.mails)
            if index > 0:
                resp, lines, octets = self.server.retr(index)
                msg_content = b'\r\n'.join(lines).decode('utf-8')  # lines存储了邮件的原始文本的每一行,可以获得整个邮件的原始文本:
                Msg = Parser().parsestr(msg_content)  # 解析出邮件:
                self.server.quit()
                self.server.close()
                return self.print_info(Msg)
            else:
                return {'Message-ID': 0}
        except Exception as err:
            print('获取邮件报错：' + str(err))
            return {'Message-ID': self.ID}

    def print_info(self, msg, indent=0):
        '''
            解析邮件内容
        :param msg:具体消息
        :param indent:用于缩进显示:
        :return:
        '''
        email_value = {}
        if indent == 0:
            for header in ['Message-ID', 'Subject', 'From', 'To']:  # 遍历获取:发件人，收件人，主题
                value = msg.get(header, '')  # 获得对应的内容
                if value:  # 有内容
                    if header == 'Subject':  # 如果是主题
                        value = self.decode_str(value)  # 解码主题
                    else:
                        hdr, addr = parseaddr(value)  # parseaddr：解析字符串中的email地址
                        name = self.decode_str(hdr)  # 解码主题
                        value = u'%s <%s>' % (name, addr)  # 合成内容
                email_value["%s%s" % ('  ' * indent, header)] = value
        return email_value

    def decode_str(self, s):
        '''
            邮件的Subject或者Email中包含的名字都是经过编码后的str,要正常显示就必须decode
        :param s:在不转换字符集的情况下解码消息头值,返回一个list
        :return:转换后数据
        '''
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value


if __name__ == '__main__':
    email = Email()
    # email.send_email('1123547734@qq.com', "雷士", "雷士台灯在线结果见附件")
    email.loop_get_data()
