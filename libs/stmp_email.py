# -*- coding: UTF-8 -*-
'''
@author: 'FenG'
@date: 2018/7/7 17:49
@file: $NAME.py
'''
from __future__ import unicode_literals

import time
import smtplib
from email.mime.text import MIMEText
from weibo_sign import sign_data
from config import Config


result = []
for data in sign_data:
    result.append('超级话题：{} 签到状态：{} 等级：{}\n'.format(data['title_sub'],data['msg'],data['desc1']))

result = ''.join(result)
msg = MIMEText(result, 'html', 'utf-8')
msg['subject'] = '{}日签到状态'.format(time.strftime("%Y-%m-%d"))

# 输入 Email 地址和口令:
from_addr = Config.from_addr
password = Config.password
# 输入收件人地址:
to_addr = Config.to_addr
# 输入 SMTP 服务器地址:
smtp_server = Config.smtp_server


server = smtplib.SMTP(smtp_server,25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()