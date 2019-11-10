# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     config
   Description :
   Author :       qiuqiu
   date：          2019/11/5
-------------------------------------------------
"""
import os

BASE_PATH = os.path.dirname(__file__)

MASTER_REMOTE_ADDR = '127.0.0.1'
MASTER_REMOTE_PORT = 8005
MASTER_REMOTE_AUTHKEY = b'proxy_key_123'

CRAWL_INTERVALS_SEC = 3

'''
ip，port(端口)，
type(类型[0高匿名，1透明])，
protocol(0 http,1 https)
'''
PROXY_TYPE_PARSE = {
    'www.66ip.cn': {
        'type': 'xpath',
        'pattern': ".//*[@id='main']/div/div[1]/table/tr[position()>1]",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': './td[4]', 'protocol': ''}
    },
    'www.kuaidaili.com': {
        'type': 'xpath',
        'pattern': ".//*[@id='list']/table/tbody/tr[position()>0]",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'}
    },
    'www.xicidaili.com': {
        'type': 'xpath',
        'pattern': ".//*[@id='ip_list']/tr[position()>1]",
        'position': {'ip': './td[2]', 'port': './td[3]', 'type': './td[5]', 'protocol': './td[6]'}
    }

}

