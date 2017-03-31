# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from_addr = 'tabqlhl@163.com'
password = 'lhl12345'
to_addr = '16621596@qq.com'
smtp_server = 'smtp.163.com'

msg = MIMEText('test email')
msg['From'] = 'From tabqlhl@163.com'
msg['To'] = 'To 16621596@qq.com'
msg['Subject'] = Header('12345')

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()