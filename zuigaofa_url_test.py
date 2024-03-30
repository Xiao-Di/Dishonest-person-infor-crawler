#!/usr/bin/env python
# coding=utf-8
'''
Author       : GengYunxin && xiaodi_shishen@163.com
Since        : 2024-03-27 22:54:13
LastEditors  : GengYunxin && xiaodi_shishen@163.com
LastEditTime : 2024-03-27 22:55:26
FilePath     : /最高法爬虫-300/dishonest/zuigaofa_url_test.py
Description  : 

Github       : https://github.com/Xiao-Di
Copyright (c) 2024 by GYX, All Rights Reserved. 
'''
import  requests
import  json
import jsonpath
# 准备请求的URL
url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'

data = {
    'pageNo': 2, # 当前页号
    'pageSize': 10, # 页面容量
    'orderBy': 1  # 排序方式
}

response = requests.post(url, data=data)
print(response.content.decode())
data =  json.loads(response.content.decode())
result = jsonpath(data, '$..data')
print(len(result[0]))