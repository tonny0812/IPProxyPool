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

BASE_PATH = os.path.dirname(__file__) + "\\"

urlsList = [
    ['http://www.66ip.cn'],
    ['https://www.kuaidaili.com/free/inha/%s/' % n for n in range(1, 11)],
    ['http://www.xicidaili.com/%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 8)]
]
