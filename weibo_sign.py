# -*- coding: UTF-8 -*-
'''
@author: 'FenG'
@date: 2018/7/7 17:27
@file: $NAME.py
'''
from __future__ import unicode_literals

import sys

from requests import session
import re
import os

USERNAME = ''  # weibo 账号
PASSWORD = ''  # weibo 密码

class WeiboSign():
    def __init__(self,USERNAME,PASSWORD):
        self.session = session()
        self.USERNAME = USERNAME
        self.PASSOWRD = PASSWORD

    def login(self):
        '''
        登录微博
        :return:
        '''
        data = {
            'username':self.USERNAME,
            'password':self.PASSOWRD
        }
        self.headers = {
            'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        login_url = 'https://passport.weibo.cn/sso/login'
        resp = self.session.post(login_url,data,headers=self.headers)

        if resp.json()['retcode'] != 20000000:
            print('登录失败，错误原因为：{}'.format(resp.json()['msg']))
            sys.exit(1)
        else:
            self.cookie = resp.headers['Set-Cookie']  # 获取cookie
            return resp.json()

    def get_chat_list(self):
        '''
        获取超级话题列表
        :return:
        '''
        chaohua_list = 'https://m.weibo.cn/api/container/getIndex?containerid=100803_-_page_my_follow_super'
        resp_list = self.session.get(chaohua_list).json()
        if resp_list['ok'] != 1:
            print('获取超级话题失败')
            sys.exit(1)
        else:
            return resp_list


    def chat_sign(self):
        '''
        话题签到
        :return:
        '''
        datas = self.get_list_data()
        result = []
        for data in datas:
            sign_url = "https://weibo.com/p/aj/general/button?api=http://i.huati.weibo.com/aj/super/checkin&id={}".format(data['id'])
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.15 Safari/537.36',
                'Cookie':self.cookie
            }
            sign_resp = self.session.get(sign_url,headers=headers).json()
            if sign_resp['code'] == '100000':
                sign_dict = {
                    'title_sub':data['title_sub'],
                    'msg':'签到成功',
                    'desc1':data['desc1']
                }
                result.append(sign_dict)
        return result
    def get_list_data(self):
        '''
        解析数据
        :return:
        '''
        datas = self.get_chat_list()
        result = list()
        card_group = datas['data']['cards'][0]['card_group'][1:-1]
        for card in card_group:
            chat_dict = {
                'id':re.findall("(?<=containerid\=)(.*)&luicode",card['scheme'])[0],
                'desc1':card['desc1'],
                'title_sub':card['title_sub'],
                'title_flag_pic':card['title_flag_pic'],

            }
            result.append(chat_dict)
        return result
if __name__ == '__main__':
    weibo = WeiboSign(USERNAME,PASSWORD)
    weibo.login()
    data = weibo.chat_sign()
    print(data)