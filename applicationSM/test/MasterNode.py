# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     MasterNode
   Description :
   Author :       qiuqiu
   date：          2019/11/10
-------------------------------------------------
"""
import time
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager


class NodeManager(object):

    def start_Manager(self, task_q, result_q):
        '''
        创建一个分布式管理器
        :param task_q: url队列
        :param result_q: 结果队列
        :return:
        '''
        # 把创建的两个队列注册在网络上，利用register方法，callable参数关联了Queue对象，
        # 将Queue对象在网络中暴露
        BaseManager.register('get_task_queue', callable=lambda: task_q)
        BaseManager.register('get_result_queue', callable=lambda: result_q)
        # 绑定端口8001，设置验证口令‘baike’。这个相当于对象的初始化
        manager = BaseManager(address=('127.0.0.1', 8001), authkey=b'test')
        # 返回manager对象
        return manager

    def main(self, task_q, result_q):
        tasks = ['test_%d' % n for n in range(1, 100)]
        print("init task queue...")
        for task in tasks:
            print(task)
            task_q.put(task)
        while True:
            try:
                if not result_q.empty():
                    result = result_q.get(True)
                    print("data from result queue: %s" % result)
                    task_q.put(result + "#" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                else:
                    time.sleep(0.1)  # 延时休息
            except BaseException as e:
                time.sleep(0.1)  # 延时休息


if __name__ == '__main__':
    manager = Manager()
    task_q = manager.Queue()
    result_q = manager.Queue()
    # 创建分布式管理器
    nodeManager = NodeManager()
    manager = nodeManager.start_Manager(task_q, result_q)
    main_proc = Process(target=nodeManager.main, args=(task_q, result_q,))
    main_proc.start()
    manager.get_server().serve_forever()
