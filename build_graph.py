import os
import json
import base64
from bs4 import BeautifulSoup
from hashlib import md5
from data_access import Driver
from config import me, data_path, data_root, encrypt

def signature(s):
    if encrypt.lower() == "true":
        m = md5()
        m.update(s.encode('utf-8'))
        return base64.encodestring(m.hexdigest()[8:-8].encode('utf-8')).decode('utf-8').strip('\n')
    else:
        return s

class User:

    def __init__(self, user=None, value=None):
        if value is None:
            self.uuid = signature(user['uuid'])
            self.nick = user['nick']
            self.cate = 'poster'
        else:
            self.uuid = value.uuid
            self.nick = value.nick
            self.cate = value.cate
    
    def get_name(self):
        return '{0}({1})'.format(self.nick, self.uuid)

    def __hash__(self):
        return hash(self.uuid)
    
    def __eq__(self, value):
        return self.uuid == value.uuid

    def json(self):
        return {'name': self.get_name(), 'category': 'me' if self.uuid == signature(me) else self.cate}
    
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

def make_index(V, E):
    vqidx = {}
    vnidx = {}
    esidx = {}
    etidx = {}
    for v in V:
        vqidx[v.uuid] = v
        vnidx[v.nick] = v
    for e in E:
        if e.src.uuid not in esidx:
            esidx[e.src.uuid] = [e]
        else:
            esidx[e.src.uuid].append(e)
        if e.tar.uuid not in etidx:
            etidx[e.tar.uuid] = [e]
        else:
            etidx[e.tar.uuid].append(e)
    return vqidx, vnidx, esidx, etidx

def filter_graph(V, E, indices, qqs=None):
    if qqs is None:
        return V, E
    vqidx, vnidx, esidx, etidx = indices
    vres = set([])
    eres = set([])
    qqs = [signature(qq) for qq in qqs]
    for qq in qqs:
        try:
            for e in esidx[qq] + etidx[qq]:
                eres.add(e)
        except KeyError as e:
            print(e)
    for e in eres:
        vres.add(e.src)
        vres.add(e.tar)
    return vres, eres

if __name__ == "__main__":
    V, E = build_graph()
    nV, nE = filter_graph(V, E, qqs=['435438602', '775789668'])
    print(nV)
    print(nE)
