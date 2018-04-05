# -*- coding: utf-8 -*-
import scrapy
from ippool.items import IppoolItem
import datetime
from ippool.tools.tools import valid_one_ip


class A66ipSpider(scrapy.Spider):
    name = '66ip'
    allowed_domains = ['66ip.cn']
    start_urls = ['http://www.66ip.cn/mo.php?tqsl={}'.format('5000')]

    def parse(self, response):
        datas = response.xpath('//body').re('(\d+\.\d+\.\d+\.\d+\:\d+)')
        print(datas)
        print(len(datas))
        for data in datas:
            item = IppoolItem()
            if valid_one_ip(data):
                item['ip'] = data
                item['source'] = '66ip'
                item['insert_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                yield item