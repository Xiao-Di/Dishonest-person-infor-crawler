#!/usr/bin/env python
# coding=utf-8
'''
Author       : GengYunxin && xiaodi_shishen@163.com
Since        : 2024-03-13 23:46:31
LastEditors  : GengYunxin && xiaodi_shishen@163.com
LastEditTime : 2024-03-13 23:50:16
FilePath     : /最高法爬虫-300/dishonest/baidu_url_test.py
Description  : 百度失信人URL测试

Github       : https://github.com/Xiao-Di
Copyright (c) 2024 by GYX, All Rights Reserved. 
'''
import requests

headers = {
        'Referer': 'https://www.baidu.com/s',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }

# 百度测试
url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人名单&pn=0&ie=utf-8&oe=utf-8&format=json'
response = requests.get(url, headers=headers)
print(response.content.decode())

# URL:
# https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人名单&pn=0&ie=utf-8&oe=utf-8&format=json
# GET
# 参数:
    # resource_id=6899: 资源id, 固定值
    # query=失信人名单: 查询内容, 固定值
    # pn=0: 数据起始号码
    # ie=utf-8&oe=utf-8: 指定数据的编码方式, 固定值
    # format=json: 数据格式, 固定值

# 数据
# {"status": "0",
# "t": "1545546994540",
# "set_cache_time": "",
# "data": [{
#     "result": [{
#         "businessEntity": "赖均朝",
#         "cardNum": "56261518-9",
#         "courtName": "中山市第二人民法院",
#         "duty": "被执行人应付262007.82元",
#         "iname": "中山市泓昊船业有限公司",
#         "publishDate": "2018年01月11日",
#         ... 
#     }],
# "otherinfo": "",
# "resNum": 50, //每一页的数据条数
# "dispNum": 100000, // 一共的数据条数
# "listNum": 2000   // 页数
# } 