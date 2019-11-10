# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ProxyWorker
   Description :
   Author :       qiuqiu
   date：          2019/11/5
-------------------------------------------------
"""
import time
from multiprocessing.managers import BaseManager

from applicationSM.spidernode import Config
from applicationSM.spidernode.HtmlDownloader import HtmlDownloader
from applicationSM.spidernode.HtmlParser import HtmlParser


class ProxyWorker(object):
    def __init__(self, name):
        self.name = name
        self.remote_addr = Config.MASTER_REMOTE_ADDR
        self.remote_port = Config.MASTER_REMOTE_PORT
        self.authkey = Config.MASTER_REMOTE_AUTHKEY
        # 初始化分布式进程中的工作节点的连接工作
        # 实现第一步：使用BaseManager注册获取Queue的方法名称
        BaseManager.register('get_url_queue')
        BaseManager.register('get_result_queue')
        # 实现第二步：连接到服务器:
        print(('Connect to server %s...' % self.remote_addr))
        # 端口和验证口令注意保持与服务进程设置的完全一致:
        self.m = BaseManager(address=(self.remote_addr, self.remote_port), authkey=self.authkey)
        # 从网络连接:
        self.m.connect()
        # 实现第三步：获取Queue的对象:
        self.url_q = self.m.get_url_queue()
        self.result_q = self.m.get_result_queue()
        # 初始化网页下载器和解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print('init finish')

    def crawl(self):
        while (True):
            try:
                if not self.url_q.empty():
                    url = self.url_q.get()
                    if url == 'end':
                        print('控制节点通知爬虫节点停止工作...')
                        return
                    print('爬虫节点(%s)正在解析:%s' % (self.name, url.encode('utf-8')))
                    content = self.downloader.download_with_no_proxies(url)
                    proxies = self.parser.parser(url, content)
                    self.result_q.put({"name": self.name, "url": url, "proxies": proxies})
                    time.sleep(Config.CRAWL_INTERVALS_SEC)
                else:
                    pass
            except EOFError as e:
                print("连接工作节点失败")
                return
            except Exception as e:
                print(e)
                print('Crawl  fali ')


if __name__ == "__main__":
    spider1 = ProxyWorker('spider1')
    spider1.crawl()
