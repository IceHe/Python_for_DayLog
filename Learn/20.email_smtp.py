#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'


# smtp
from email.mime.text import MIMEText
msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')

# from_addr = b'290841032@qq.com'
# pwd = b'/*icy34244394'
#
# to_addr = b'ice_he@foxmail.com'
# smtp_server = b'smtp.qq.com'

# 输入Email地址和口令:
from_addr = input('From: ')
pwd = input('Password: ')
# 输入收件人地址:
to_addr = input('To: ')
# 输入SMTP服务器地址:
smtp_server = input('SMTP server: ')

import smtplib
server = smtplib.SMTP(smtp_server, 465)
server.set_debuglevel(1)
server.starttls()
server.login(from_addr, pwd)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
print('send end.')

# 未知错误，无法运行，不打算尝试，继续学习往后的内容。