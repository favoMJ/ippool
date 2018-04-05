# -*- coding: utf-8 -*-
import scrapy
import datetime
from ippool.items import IppoolItem
from ippool.tools.tools import valid_one_ip


# 不能太快，会被封
class KuaidailiSpider(scrapy.Spider):
    name = 'kuaidaili'
    allowed_domains = ['kuaidaili.com']
    start_urls = ['https://www.kuaidaili.com/free/inha/{}/'.format(str(i)) for i in range(1, 10+1)] + ['https://www.kuaidaili.com/free/intr/{}/'.format(str(i)) for i in range(1, 10+1)]
    headers = {
        'Host': 'www.kuaidaili.com',
        'Referer': 'https://www.kuaidaili.com/free/inha/5/',
        'Cookie': '__guid=90492700.3724539585886129700.1522854548319.581; channelid=0; sid=1522862068821540; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1522862071; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1522864018; _ga=GA1.2.786754394.1522862071; _gid=GA1.2.1779524082.1522862071; _gat=1; monitor_count=53',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        # "User-Agent": UserAgent().random,
    }
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': headers,  # 单独设置headers,避免与其他爬虫冲突,但会覆盖中间件的设置
        'DOWNLOAD_DELAY': 10,
    }

    def parse(self, response):
        datas = response.xpath('//*[@id="list"]/table/tbody/tr')
        for data in datas:
            item = IppoolItem()
            host = data.xpath('td[1]/text()').extract()[0]
            port = data.xpath('td[2]/text()').extract()[0]
            ip = host+':'+port
            if valid_one_ip(ip):
                item['ip'] = ip
                item['source'] = 'kuaidaili'
                item['insert_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(item)
                yield item


# start_urls = ['https://www.kuaidaili.com/free/inha/{}/'.format(str(i)) for i in range(1, 20+1)]
# print(start_urls)