# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     HtmlParser
   Description :
   Author :       qiuqiu
   date：          2019/11/5
-------------------------------------------------
"""
from urllib.parse import urlsplit
from xml import etree

from bs4 import BeautifulSoup

from applicationSM.spidernode.Config import PROXY_TYPE_PARSE


class HtmlParser(object):

    def parser(self, page_url, html_cont):
        '''
        用于解析网页内容抽取URL和数据
        :param page_url: 下载页面的URL
        :param html_cont: 下载的网页内容
        :return:返回代理数据
        '''
        if page_url is None or html_cont is None:
            return

        parser = self._get_proxy_parser(page_url)
        proxy_datas = self._get_proxies(parser, html_cont)
        return proxy_datas

    def _get_proxies(self, parser, html_cont):
        if parser['type'] == 'xpath':
            return self._XpathPraser(html_cont, parser)

    def _get_proxy_parser(self, page_url):
        split_url = urlsplit(page_url)
        parser = PROXY_TYPE_PARSE[split_url.netloc]
        return parser

    def _XpathPraser(self, html_cont, parser):
        '''
        针对xpath方式进行解析
        :param html_cont:
        :param parser:
        :return:
        '''
        proxylist = []
        root = etree.HTML(html_cont)
        proxys = root.xpath(parser['pattern'])
        for proxy in proxys:
            try:
                ip = proxy.xpath(parser['position']['ip'])[0].text
                port = proxy.xpath(parser['position']['port'])[0].text
                type = 0
                protocol = 0
            except Exception as e:
                continue
            proxy = {'ip': ip,
                     'port': int(port),
                     'type': int(type),
                     'protocol': int(protocol)
                     }
            proxylist.append(proxy)
        return proxylist

    def _SoupPraser(self, html_cont, parser):
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
