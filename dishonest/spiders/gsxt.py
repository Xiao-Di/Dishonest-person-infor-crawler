#!/usr/bin/env python
# coding=utf-8
'''
Author       : GengYunxin && xiaodi_shishen@163.com
Since        : 2024-03-31 00:39:16
LastEditors  : GengYunxin && xiaodi_shishen@163.com
LastEditTime : 2024-03-31 00:53:16
FilePath     : /最高法爬虫-300/dishonest/dishonest/spiders/gsxt.py
Description  : 

Github       : https://github.com/Xiao-Di
Copyright (c) 2024 by GYX, All Rights Reserved. 
'''
import scrapy
import json
import re
from datetime import datetime

from dishonest.items import DishonestItem

class GsxtSpider(scrapy.Spider):
    name = 'gsxt'
    allowed_domains = ['gsxt.gov.cn']
    # 准备起始
    start_urls = ['http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html']

    custom_settings = {
        'DOWNLOAD_DELAY' : 5
    }

    def parse(self, response):
        # 获取城市标签的div列表
        divs = response.xpath('//*[@id="qysx"]/div[3]/div')
        # 遍历divs, 获取城市id和名称
        for div in divs:
            area_id = div.xpath('./@id').extract_first()
            area_name = div.xpath('./label/text()').extract_first()
            # 准备请求的URL
            url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?' \
                  'noticeType=11&areaid=100000&noticeTitle=&regOrg={}'.format(area_id)
            # 一个城市最多能够获取50条数据.
            for i in range(0, 50, 10):
                data = {
                    'start': str(i)
                }
                # 构建请求, 交给引擎
                yield scrapy.FormRequest(url, formdata=data, callback=self.parse_data,
                                         meta={'area_name': area_name})

    def parse_data(self, response):
        # print(response.text)
        """解析页面中的城市"""
        area_name = response.meta['area_name']
        result = json.loads(response.text)
        datas = result['data']
        for data in datas:
            item = DishonestItem()
            # 区域名称
            item['area_name'] = area_name
            # 公告标题
            notice_title = data['noticeTitle']
            name = re.findall('关?于?(.+?)的?列入', notice_title)[0]
            item['name'] = name
            notice_content = data['noticeContent']
            card_id = re.findall('经查.+[（\(]统一社会信用码/注册号：(\w+)[）\)]', notice_content)
            item['card_num'] = card_id[0] if len(card_id) != 0 else ''
            item['content'] = notice_content
            # 公布单位
            item['publish_unit'] = data['judAuth_CN']
            # 获取到的时间, 是1970年1月1日 0时0分0秒 到发布时间的毫秒数
            publish_ms = data['noticeDate']
            # 转换为日期类型
            publish_date = datetime.fromtimestamp(publish_ms / 1000)
            item['publish_date'] = publish_date.strftime('%Y年%m月%d日')
            yield item
