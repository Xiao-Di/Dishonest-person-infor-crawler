#!/usr/bin/env python
# coding=utf-8
'''
Author       : GengYunxin && xiaodi_shishen@163.com
Since        : 2024-03-13 23:40:09
LastEditors  : GengYunxin && xiaodi_shishen@163.com
LastEditTime : 2024-03-27 22:35:17
FilePath     : /最高法爬虫-300/dishonest/dishonest/middlewares.py
Description  : 

Github       : https://github.com/Xiao-Di
Copyright (c) 2024 by GYX, All Rights Reserved. 
'''
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import requests
from dishonest.settings import USER_AGENTS

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class RandomUserAgent(object):
    def process_request(self, request, spider):
        """
            设置随机的User-Agent
        """
        if request.url.startswith('https://cdnware.m.jd.com'):
            # 如果使用手机抓包, 获取到商品信息; 生成请求请求头
            number  = random.uniform(100000,199999)
            request.headers['user-agent'] = 'JD4iPhone/{} (iPhone; iOS 12.1.2; Scale/2.00)'.format(number)
        else:
            # 随机获取一个请求头, 进行设置
            request.headers['user-agent'] = random.choice(USER_AGENTS)

# 代理下载器中间件
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # 发送请求获取代理IP
        # params = {
        #     'protocol':'https'
        # }
        protocol = request.url.split('://')[0]
        proxy_url = 'http://localhost:6868/random?protocol={}'.format(protocol)

        response = requests.get(proxy_url)
        proxy  = response.content.decode()
        request.meta['proxy'] = proxy
        return None