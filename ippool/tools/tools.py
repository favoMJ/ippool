# -*- coding:utf-8 -*-
"""
@author:kkh
@file:tools.py
@time:2018/4/422:39
"""
import requests


# 验证单个ip,返回True或False
def valid_one_ip(ip: str):
    url = 'http://www.baidu.com'
    proxies = {
        'http': ip,
    }
    # 校验两次
    try:
        if requests.request(method='GET', url=url, timeout=1, proxies=proxies).status_code == 200:
            return True
        else:
            return False
    except:
        try:
            if requests.request(method='GET', url=url, timeout=1, proxies=proxies).status_code == 200:
                return True
            else:
                return False
        except:
            return False


# 验证ip列表,返回可用列表
def valid_many_ip(ip_list: list):
    ip_res = []
    if len(ip_list) == 0 or ip_list is None:
        return ip_res
    print('待验证列表:', ip_list)
    for i in range(len(ip_list)):
        print('验证第{}个ip'.format(str(i)))
        usable = valid_one_ip(ip_list[i])  # 验证该ip是否可用
        if usable:
            print('{}可用'.format(ip_list[i]))
            ip_res.append(ip_list[i])
            ip_res = list(set(ip_res))
    return ip_res


print(valid_one_ip('59.44.164.34:3128') is True)