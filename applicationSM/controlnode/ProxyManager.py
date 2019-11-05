# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ProxyManager
   Description :
   Author :       qiuqiu
   date：          2019/11/5
-------------------------------------------------
"""

import hashlib
import pickle

from applicationSM.controlnode.Config import BASE_PATH


class ProxyManager(object):
    def __init__(self):
        self.new_proxies = self.load_progress(BASE_PATH + 'files\\new_proxies.txt')  # 未爬取到的代理集合
        self.old_proxes = self.load_progress(BASE_PATH +'files\\old_proxies.txt')  # 已爬取到的代理集合

    def add_new_proxy(self, proxy):
        '''
         将新的URL添加到未爬取的URL集合中
        :param url:单个URL
        :return:
        '''
        if proxy is None:
            return
        m = hashlib.md5()
        m.update(proxy.encode('utf-8'))
        url_md5 = m.hexdigest()[8:-8]
        if proxy not in self.new_proxies and url_md5 not in self.old_proxes:
            self.new_proxies.add(proxy)

    def add_new_proxies(self, proxies):
        '''
        将新的URLS添加到未爬取的URL集合中
        :param urls:url集合
        :return:
        '''
        if proxies is None or len(proxies) == 0:
            return
        for proxy in proxies:
            self.add_new_proxy(proxy)

    def new_proxy_size(self):
        '''
        获取新代理集合的大小
        :return:
        '''
        return len(self.new_proxies)

    def old_proxy_size(self):
        '''
        获取已经爬取URL集合的大小
        :return:
        '''
        return len(self.old_proxes)

    def save_progress(self, path, data):
        '''
        保存进度
        :param path:文件路径
        :param data:数据
        :return:
        '''
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load_progress(self, path):
        '''
        从本地文件加载进度
        :param path:文件路径
        :return:返回set集合
        '''
        print('[+] 从文件加载进度: %s' % path)
        try:
            with open(path, 'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except :
            print('[!] 无进度文件, 创建: %s' % path)
        return set()