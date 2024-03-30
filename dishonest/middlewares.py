#!/usr/bin/env python
# coding=utf-8
'''
Author       : GengYunxin && xiaodi_shishen@163.com
Since        : 2024-03-13 23:40:09
LastEditors  : GengYunxin && xiaodi_shishen@163.com
LastEditTime : 2024-03-31 00:45:40
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
from dishonest.spiders.gsxt import GsxtSpider

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class RandomUserAgent(object):
    def process_request(self, request, spider):
        """
        设置随机的User-Agent
        """
        # 如果spider是公示系统spider，就直接跳过
        if isinstance(spider, GsxtSpider):
            return None
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
        # 如果spider是公示系统spider，就直接跳过
        if isinstance(spider, GsxtSpider):
            return None
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
    
import time
import re
import js2py
# 企业信用公示系统中间件
class GsxtMiddleware(object):
    # 1. 定义一个类变量列表, 用于存储cookie信息
    cookie = {}
    # 2. 定义cookie字典中使用的三个键
    cookie_key = 'cookie'
    user_agent_key = 'user_agent'
    proxy_key = 'proxy'

    def get_new_cookie(self):
        # 公告子页面URL
        url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
        while True:
            try:
                # 随机获取一个User-Agent
                user_agent = random.choice(USER_AGENTS)

                # 从代理池随机获取一个代理IP
                params = {'protocol': 'http', 'domain':'gsxt.gov.cn'}
                response = requests.get('http://localhost:6868/random', params=params)
                # 准备代理
                proxy = response.content.decode()

                headers = {
                    'User-Agent': user_agent
                }

                # 获取发送请求的session对象
                session = requests.session()
                # 设置请求头
                session.headers = headers

                # 设置代理IP
                session.proxies = {'http': proxy}
                # 发送请求, 获取cookie信息, 设置超时参数
                response = session.get(url, timeout=5)
                # 第一个cookie信息
                print('='*100)
                # 提取 script标签中js
                js = re.findall('<script>(.+)</script>', response.content.decode())
                if len(js) != 0:
                    js = js[0]
                    # print(js)
                    js = js.replace('eval', 'code = ')
                    # print(js)
                    # 获取js的执行环境
                    context = js2py.EvalJs()
                    print(context.execute(js))
                    # 截取生成cookie那段代码
                    code = re.findall(r"document.(cookie=.+())\+';", context.code)[0][0]
                    # print(code)
                    # 执行生成cookie的代码
                    context.execute(code)
                    # 切割当前cookie的name 和 value
                    name, value = context.cookie.split('=')
                    # 把cookie信息设置给session
                    session.cookies.set(name, value)
                    # 再次构建请求, 获取后面的cookie信息
                    response = session.get(url)
                    # 把session中cookie信息转为字典

                    cookies = requests.utils.dict_from_cookiejar(session.cookies)
                    # 把生成user_agent, 代理IP,  cookie, 放到一个字典中, 然后添加到列表
                    self.cookie = {
                        self.proxy_key: proxy,
                        self.cookie_key:cookies,
                        self.user_agent_key:user_agent
                    }
                    print('*'*100)
                    time.sleep(3)
                    break
            except Exception as ex:
                print(ex)
                if proxy:
                    self.disable_domain(proxy)

    def disable_domain(self, proxy):
        ip = re.findall('http://(.+):\d+', proxy)
        params = {
            'ip': ip,
            'domain': 'gsxt.gov.cn'
        }
        # 获取代理IP, 标注该域名下代理IP不可用
        requests.get('http://localhost:6868/disable_domain', params=params)

    def process_request(self, request, spider):
        # 如果是公告系统
        if isinstance(spider, GsxtSpider):

            # 从池中随机获取一套cookie信息
            if not self.cookie:
                self.get_new_cookie()

            print(self.cookie)
            # 使用这套cookie信息, 设置request
            request.headers['User-Agent'] = self.cookie[self.user_agent_key]
            request.cookies = self.cookie[self.cookie_key]
            request.meta['proxy'] = self.cookie[self.proxy_key]
            # 关闭重定向
            request.meta['dont_redirect'] = True
            # request.meta['cookiejar'] = self.cookie[self.proxy_key]

    def process_response(self, request, response, spider):
        """处理响应"""
        if isinstance(spider, GsxtSpider):
            # print(response.status)
            if response.status != 200 or not response.body:
                # 重新获取一个新的cookie
                self.get_new_cookie()

                req = request.copy()
                req.dont_filter = True
                # 重写构建请求
                return req

        # 返回响应数据
        return response