# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from scrapy.conf import settings


class IppoolPipeline(object):

    def __init__(self):
        host = settings['REDIS_HOST']
        port = settings['REDIS_PORT']
        password = settings['REDIS_PASSWD']
        db = settings['REDIS_DB']
        self.rds = redis.Redis(host=host, port=port,password=password,db=db)

    def process_item(self, item, spider):
        self.rds.lpush('proxies', item)
        return item
