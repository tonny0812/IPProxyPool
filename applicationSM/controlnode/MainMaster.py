# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ProxyMaster
   Description :
   Author :       qiuqiu
   date：          2019/11/5
-------------------------------------------------
"""

from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue
import time

from applicationSM.controlnode import Config
from applicationSM.controlnode.ProxyManager import ProxyManager

q_num = 20
url_q = Queue(q_num)
result_q = Queue(q_num * 10)
store_q = Queue(q_num * 10)

# 替代原来的匿名函数
def get_url_queue():
    return url_q


# 替代原来的匿名函数
def get_result_queue():
    return result_q


class MainMaster(object):

    def start_Manager(self):

        '''
        创建一个分布式管理器
        :param url_q: url队列
        :param result_q: 结果队列
        :return:
        '''
        # 把创建的两个队列注册在网络上，利用register方法，callable参数关联了Queue对象，
        # 将Queue对象在网络中暴露
        # BaseManager.register('get_url_queue', callable=lambda: url_q)
        # BaseManager.register('get_result_queue', callable=lambda: result_q)
        BaseManager.register('get_url_queue', callable=get_url_queue)
        BaseManager.register('get_result_queue', callable=get_result_queue)
        # 绑定端口8001，设置验证口令‘proxy_key_123’。这个相当于对象的初始化
        manager = BaseManager(address=('127.0.0.1', 8005), authkey=b'proxy_key_123')
        # 返回manager对象
        return manager

    def proxy_url_proc(self):
        for urls in Config.urlsList:
            for url in urls:
                # 将新的URL发给工作节点
                print(url)
                try:
                    url_q.put(url)
                except Exception as e:
                    print(e)
                time.sleep(0.1)
        url_q.put('end')

    def proxy_result_proc(self):
        proxy_manager = ProxyManager()
        while (True):
            try:
                if not result_q.empty():
                    # Queue.get(block=True, timeout=None)
                    proxies = result_q.get(True)
                    proxy_manager.add_new_proxies(proxies)
                    for proxy in proxies:
                        store_q.put(proxy)  # 解析出来的数据为dict类型
                else:
                    print(url_q.qsize())
                    time.sleep(5)  # 延时休息
            except BaseException as e:
                time.sleep(0.1)  # 延时休息

    def store_proc(self):
        while True:
            if not store_q.empty():
                proxy = store_q.get()
                print("代理商信息：%s" % proxy)
            else:
                time.sleep(0.1)
        pass


if __name__ == '__main__':

    # 创建分布式管理器
    master = MainMaster()
    manager = master.start_Manager()
    # 创建URL管理进程、 数据提取进程和数据存储进程
    url_manager_proc = Process(target=master.proxy_url_proc, args=())
    result_manager_proc = Process(target=master.proxy_result_proc, args=())
    store_proc = Process(target=master.store_proc, args=())
    # 启动进程和分布式管理器
    url_manager_proc.start()
    result_manager_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()
