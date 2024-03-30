# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from datetime import datetime

from dishonest.settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT
from dishonest.spiders.gsxt import GsxtSpider

"""
在open_spider中, 建立数据库连接, 获取操作的数据的cursor
在process_item中, 如果数据不存, 保存数据;
在close_spider中, 关闭cursor,关闭数据库连接
"""
class DishonestPipeline:
    def open_spider(self, spider):
        # 创建数据链接
        self.connect = pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER, password=MYSQL_PASSWORD,
                                       db=MYSQL_DB, port=MYSQL_PORT)
        # 获取执行SQL的cursor
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        # 释放游标
        self.cursor.close()
        # 释放链接
        self.connect.close()

    def process_item(self, item, spider):
        if item['age'] == 0:
            # 企业， 根据企业名称和区域进行判断
            select_count_sql = "SELECT COUNT(1) from dishonest WHERE name = '{} ' and area = '{}'".format(item['name'], item['area'])
        else: # 否则就是自然人
            # 根据证件号, 数据条数
            select_count_sql = "SELECT COUNT(1) from dishonest WHERE card_num='{}'".format(item['card_num'])
        
        # 执行查询SQL
        self.cursor.execute(select_count_sql)
        # 获取查询结果
        count = self.cursor.fetchone()[0]

        # 百度爬到的身份证号中间是3个*，将最高法爬到的完整身份证号也加*做统一处理
        card_num = item['card_num']
        # 居民身份证号是18为, 为了和百度抓取数据做到兼容, 修改为百度个格式
        if len(card_num) == 18:
            card_num = card_num[:-7] + '****' + card_num[-4:]
            # 修改身份证号, 为百度的格式, 方便后续的数据去重 和 保护失信人隐私.
            item['card_num'] = card_num

        # 根据国家信息公示系统，增加区域和地区查询条件
        if isinstance(spider, GsxtSpider):
            # 由于在`国家企业信用公布系统`的公告信息中, 没有企业代码或信用号, 所以在这里采用地区加企业名称的方式查询
            name = item['name']
            area_name = item['area_name']
            select_sql = "select count(1) from dishonest where name='{}' and area_name='{}'".format(name, area_name)
        else:
            # 根据证件号, 数据条数
            select_sql = "select count(1) from dishonest where card_num='{}'".format(item['card_num'] )
        # 去重
        # 如果查询的数量为0, 说明该人不存在, 不存在就插入
        if count == 0:
            # # 获取当前的时间, 为插入数据库的时间
            # item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 把数据转换为键, 值的格式, 方便插入数据库
            keys, values = zip(*dict(item).items())
            # 插入数据库SQL
            insert_sql = 'INSERT INTO dishonest ({}) VALUES({})'.format(
                ','.join(keys),
                ','.join(['%s'] * len(values))
            )
            # 执行插入数据SQL
            self.cursor.execute(insert_sql, values)
            # 提交
            self.connect.commit()
            spider.logger.info('插入数据成功')
        else:
            spider.logger.info('{}  重复'.format(item))
        return item
