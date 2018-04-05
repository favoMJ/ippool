# -*- coding:utf-8 -*-
"""
@author:kkh
@file:main.py
@time:2018/4/52:44
"""
from scrapy import cmdline
import os


command = 'scrapy list'
lines = os.popen(command).readlines()[1:]
lines = [i[:-1] for i in lines]
print(lines)

for spider in lines:
    # print('scrapy crawl {}'.format(spider))
    cmdline.execute('scrapy crawl {}'.format(spider).split())

