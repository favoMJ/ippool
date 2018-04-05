import re
import redis
import time
import requests


class RedisClient(object):
    def __init__(self ):
        self._db = redis.Redis(host='localhost', port='6379',password='favomj',db=2)

    def get(self, count=1):
        proxies = self._db.lrange("proxies", 0, count - 1)
        self._db.ltrim("proxies", count, -1)
        proxies = map(lambda x:x.decode('utf8') , proxies)
        return set(proxies)

    def put(self, proxy):
        self._db.rpush("proxies", proxy)

    def _put(self,proxy):
        for p in proxy:
            self._db.rpush("_proxies", p)

    def test_ip(self,ip, test_url='http://2017.ip138.com/ic.asp', time_out=1):
        proxies = {'http': ip}
        try_ip = ip.split(':')[0]
        try:
            r = requests.get(test_url, proxies=proxies, timeout=time_out)
            if r.status_code == 200:
                r.encoding = 'gbk'
                result = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', r.text)
                result = result.group()
                if result[:9] == try_ip[:9]:
                    print(ip,'测试通过')
                    return True
                else:
                    #print('%s:%s 携带代理失败,使用了本地IP' % (ip[0], ip[1]))
                    return False
            else:
                #print('%s:%s 请求码不是200' % (ip[0], ip[1]))
                return False
        except:
            #print('%s:%s 请求过程错误' % (ip[0], ip[1]))
            return False

    def _yz(self):
        _proxy = self._db.lrange('_proxies',0,-1)
        _proxy = set(map(lambda x: x.decode('utf8').strip(), _proxy))

        if not _proxy or not len(_proxy):return
        self._db.ltrim("_proxies", len(_proxy) , -1)
        list(map(lambda x:self.put(x) if self.test_ip(eval(x)['ip']) else 0, _proxy))

    def db_len(self):
        return self._db.llen('proxies')

    def _trans(self):
        count = self.db_len()
        temp = self.get(count)
        self._put(temp)

    def _test(self):
        self._trans()
        self._yz()

    def run(self):
        while 1:
            self._trans()
            self._yz()
            time.sleep(600)

    def pop(self):
        try:
            return self._db.rpop("proxies").decode('utf-8')
        except:
            pass


if __name__ == '__main__':
    rc = RedisClient()
    rc.run()
