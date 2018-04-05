# -*- coding: utf-8 -*-
import scrapy
import datetime
from fake_useragent import UserAgent
from ippool.tools.tools import valid_one_ip
from ippool.items import IppoolItem


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/wt/{}'.format(str(i)) for i in range(1, 11)]
    headers = {
        'User-Agent': UserAgent().random,
        'Referer': 'http://www.xicidaili.com/wt',
    }
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': headers,  # 单独设置headers,避免与其他爬虫冲突,但会覆盖中间件的设置
    }

    def parse(self, response):
        datas = response.xpath('//*[@id="ip_list"]/tr')
        for data in datas[1:]:
            host = data.xpath('td[2]/text()').extract()[0]
            port = data.xpath('td[3]/text()').extract()[0]
            ip = host + ':' + port
            if valid_one_ip(ip):
                item = IppoolItem()
                item['ip'] = ip
                item['source'] = 'xici'
                item['insert_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                yield item