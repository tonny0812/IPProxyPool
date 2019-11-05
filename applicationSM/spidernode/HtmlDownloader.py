# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     HtmlDownloader
   Description :   网页下载器
   Author :       qiuqiu
   date：          2019/11/5
-------------------------------------------------
"""
from applicationSM.utils import RequestUtil


class HtmlDownloader(object):

    def download_with_no_proxies(self, url):
        return RequestUtil.download_content(url, proxies=None, timeout=10)