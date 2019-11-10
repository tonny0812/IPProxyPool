# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     SlaveNode
   Description :
   Author :       qiuqiu
   date：          2019/11/10
-------------------------------------------------
"""
import time
from multiprocessing.managers import BaseManager


class NodeManager(object):

    def __init__(self, name):
        self.name = name
        # 初始化分布式进程中的工作节点的连接工作
        # 实现第一步：使用BaseManager注册获取Queue的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        # 实现第二步：连接到服务器:
        server_addr = '127.0.0.1'
        print(('Connect to server %s...' % server_addr))
        # 端口和验证口令注意保持与服务进程设置的完全一致:
        self.m = BaseManager(address=(server_addr, 8001), authkey=b'test')
        # 从网络连接:
        self.m.connect()
        # 实现第三步：获取Queue的对象:
        self.task_q = self.m.get_task_queue()
        self.result_q = self.m.get_result_queue()
        print('init finish')

    def main(self):
        while True:
            try:
                if not self.task_q.empty():
                    task_content = self.task_q.get()
                    print('节点(%s)获取:%s' % (self.name, task_content.encode('utf-8')))
                    result = task_content + "_" + self.name + "@" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    self.result_q.put(result)
            except EOFError as e:
                print("连接工作节点失败")
                return
            except Exception as e:
                print(e)
                print('slave  fail ')

if __name__ == '__main__':
    slaveNode = NodeManager('slave_1')
    slaveNode.main()