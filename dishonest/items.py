#!/usr/bin/env python
# coding=utf-8
'''
Author       : GengYunxin && xiaodi_shishen@163.com
Since        : 2024-03-13 23:40:09
LastEditors  : GengYunxin && xiaodi_shishen@163.com
LastEditTime : 2024-03-14 10:49:10
FilePath     : /最高法爬虫-300/dishonest/dishonest/items.py
Description  : 

Github       : https://github.com/Xiao-Di
Copyright (c) 2024 by GYX, All Rights Reserved. 
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DishonestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 姓名/获取企业名称
    name = scrapy.Field()
    age = scrapy.Field()
    area = scrapy.Field()
    # 证件号
    card_num = scrapy.Field()
    # 失信内容
    content = scrapy.Field()
    # 法人
    business_entity = scrapy.Field()
    # 公布单位/执行单位
    publish_unit = scrapy.Field()
    # 公布日期/宣判日期
    publish_date= scrapy.Field()
    # 更新日期, 创建日期
    create_date = scrapy.Field()
    # 更新日期
    update_date = scrapy.Field()
