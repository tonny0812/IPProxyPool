# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ProxyMaster
   Description :
   Author :       qiuqiu
   date：          2019/11/5
-------------------------------------------------
"""

import time
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

from applicationSM.controlnode import Config


class MainMaster(object):

    def start_Manager(self, url_q, result_q):

        '''
        创建一个分布式管理器
        :param url_q: url队列
        :param result_q: 结果队列
        :return:
        '''
        # 把创建的两个队列注册在网络上，利用register方法，callable参数关联了Queue对象，
        # 将Queue对象在网络中暴露
        BaseManager.register('get_url_queue', callable=lambda: url_q)
        BaseManager.register('get_result_queue', callable=lambda: result_q)
        # 绑定端口8005，设置验证口令‘proxy_key_123’。这个相当于对象的初始化
        manager = BaseManager(address=('127.0.0.1', 8005), authkey=b'proxy_key_123')
        # 返回manager对象
        return manager

    def proxy_url_proc(self, url_q, retry_url_q):
        for urls in Config.urlsCrawlList:
            for url in urls:
                # 将新的URL发给工作节点
                print("put url(%s) into url_q" % url)
                url_q.put(url)
                time.sleep(2)
        while True:
            if not retry_url_q.empty():
                print("put retry url(%s) into url_q" % url)
                url_q.put(url)
                time.sleep(Config.RETRY_INTERVAL_SEC)



    def proxy_result_proc(self, retry_url_q, result_q, store_q):
        # proxy_manager = ProxyManager()
        while (True):
            try:
                if not result_q.empty():
                    result = result_q.get(True)
                    # print(result)
                    if result['proxies'] is None:
                        print("url(%s) get None" % result['url'])
                        retry_url_q.put(result['url'])
                    else:
                        # proxy_manager.add_new_proxies(proxies)
                        for proxy in result['proxies']:
                            store_q.put(proxy)  # 解析出来的数据为dict类型
                else:
                    print(url_q.qsize())
                    time.sleep(5)  # 延时休息
            except BaseException as e:
                time.sleep(0.1)  # 延时休息

    def store_proc(self, store_q):
        with open(file=Config.PROXIES_FILE_PATH, mode="a+", encoding="UTF-8") as fileWrapper:
            while True:
                if not store_q.empty():
                    proxy = store_q.get()
                    # print("代理商信息：%s" % proxy)
                    fileWrapper.write(str(proxy))
                    fileWrapper.write('\n')
                else:
                    time.sleep(0.1)


if __name__ == '__main__':
    manager = Manager()
    url_q = manager.Queue()
    retry_url_q = manager.Queue()
    result_q = manager.Queue()
    store_q = manager.Queue()
    # 创建分布式管理器
    master = MainMaster()
    manager = master.start_Manager(url_q, result_q)
    # 创建URL管理进程、 数据提取进程和数据存储进程
    url_manager_proc = Process(target=master.proxy_url_proc, args=(url_q,retry_url_q,))
    result_manager_proc = Process(target=master.proxy_result_proc, args=(retry_url_q, result_q, store_q,))
    store_proc = Process(target=master.store_proc, args=(store_q,))
    # 启动进程和分布式管理器
    url_manager_proc.start()
    result_manager_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()
