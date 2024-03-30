#!/usr/bin/env python
# coding=utf-8
'''
Author       : GengYunxin && xiaodi_shishen@163.com
Since        : 2024-03-27 22:57:11
LastEditors  : GengYunxin && xiaodi_shishen@163.com
LastEditTime : 2024-03-27 23:05:30
FilePath     : /最高法爬虫-300/dishonest/dishonest/spiders/court.py
Description  : 

Github       : https://github.com/Xiao-Di
Copyright (c) 2024 by GYX, All Rights Reserved. 
'''
import scrapy
import json
import datetime

from dishonest.items import DishonestItem


class CourtSpider(scrapy.Spider):
    name = 'court'
    allowed_domains = ['court.gov.cn']
    # POST请求的URL
    post_url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'

    def start_requests(self):
        """构建起始请求"""
        data = {
            'pageNo': '1',  # 当前页号
            'pageSize': '10',  # 页面容量
            'orderBy': '1'  # 排序方式
        }
        # 构建起始POST请求
        yield scrapy.FormRequest(self.url, formdata=data,  callback=self.parse)


    def parse(self, response):
        # 获取总页数
        page_count = json.loads(response.text)['pageCount']
        # 生成所有页面请求
        for i in range(1, page_count):
            data = {
                'pageNo': str(i),  # 当前页号
                'pageSize': '10',  # 页面容量
                'orderBy': '1'  # 排序方式
            }
            yield scrapy.FormRequest(self.url, formdata=data, callback=self.parse_data)


    def parse_data(self, response):
        """解析响应数据"""
        datas = json.loads(response.text)['data']
        for data in datas:
            item = DishonestItem()
            # 把抓取到数据, 交给引擎
            item['name'] = data['name'] # 名称
            item['card_num'] = data['cardNum'] # 号码
            item['age'] = data['age'] # 年龄 
            item['area_name'] = data['areaName'] # 区域
            item['content'] = data['duty'] # 失信内容
            item['business_entity'] = data['buesinessEntity'] # 法人（企业）
            item['publish_unit'] = data['courtName'] # 公布单位
            item['publish_date'] = data['publishDate'] # 公布日期
            item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 创建日期
            item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 更新日期
            # print(item)
            # 把数据交给引擎
            yield item
