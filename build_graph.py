import os
import json
from bs4 import BeautifulSoup
from data_access import Driver
from config import me, data_path, data_root

class User:

    def __init__(self, user):
        self.uuid = user['uuid']
        self.nick = user['nick']
        self.cate = 'poster'
    
    def get_name(self):
        return '{0}({1})'.format(self.nick, self.uuid)

    def __hash__(self):
        return hash(self.uuid)
    
    def __eq__(self, value):
        return self.uuid == value.uuid

    def json(self):
        return {'name': self.get_name(), 'category': 'me' if self.uuid == me else self.cate}
    
    def __str__(self):
        return json.dumps(self.json(), ensure_ascii=False)

    def __repr__(self):
        return json.dumps(self.json(), ensure_ascii=False)

class Edge:

    def __init__(self, src, tar):
        self.src: User = src
        self.tar: User = tar
    
    def _mima(self):
        mi = min(self.src.uuid, self.tar.uuid)
        ma = max(self.src.uuid, self.tar.uuid)
        return mi, ma

    def __hash__(self):
        mi, ma = self._mima()
        return hash(mi + '-' + ma)
    
    def __eq__(self, value):
        mi1, ma1 = self._mima()
        mi2, ma2= value._mima()
        return mi1 == mi2 and ma1 == ma2
    
    def json(self):
        return {'source': '{0}({1})'.format(self.src.nick, self.src.uuid), 'target': '{0}({1})'.format(self.tar.nick, self.tar.uuid)}
    
    def __str__(self):
        return json.dumps(self.json(), ensure_ascii=False)

    def __repr__(self):
        return json.dumps(self.json(), ensure_ascii=False)

def build_graph():
    V = set([])
    E = set([])
    driver = Driver()
    count = 0
    for i in os.walk(data_root + data_path):
        count = len(i[2])
    for i in range(count):
        htmls = driver.fetch_html_list(i)
        for html in htmls:
            soup = BeautifulSoup(html, 'lxml')
            for li in soup.findAll('li'):
                try:
                    poster = User(driver.get_user(li))
                    poster.cate = 'poster'
                    V.add(poster)
                    for liker_json in driver.get_liker_list(li):
                        liker = User(liker_json)
                        if liker not in V:
                            liker.cate = 'liker'
                            V.add(liker)
                        E.add(Edge(poster, liker))
                except:
                    pass
    return V, E
