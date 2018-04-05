import redis
import random

class IPool():
    def update(self):
        _proxy = self._db.lrange('proxies', 0, -1)
        _proxy = set(map(lambda x: x.decode('utf8'), _proxy))
        if not _proxy or not len(_proxy): return
        list(map(lambda x: self._ip.append(x), _proxy))

    def __init__(self):
        self._db = redis.Redis(host='47.94.141.99', port='6379',password='favomj',db=2)
        self._ip = []
        self.update()

    def __getitem__(self, position):
        return eval(str(self._ip[position]))['ip']

    @property
    def ip(self):
        if(len(self._ip)):
            return eval(random.choice(self._ip))['ip']

if __name__ == '__main__':
    ips = IPool()
    print(ips.ip)