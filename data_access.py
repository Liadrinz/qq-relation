import json
from bs4 import BeautifulSoup

from config import data_path, data_root, me

class Driver:

    def __init__(self):
        self._cache = {}
    
    def fetch_html_list(self, index):
        if index in self._cache:
            return self._cache[index]
        with open('{0}/{1}/html_chunk{2}.json'.format(data_root, data_path, index), 'rb') as f:
            data = json.loads(f.read())
            self._cache[index] = data
            return data
    
    def get_user(self, soup: BeautifulSoup):
        try:
            link = soup.find('a', {'data-clicklog': 'nick'})
            nick = link.text
            uuid = link['href'].split('/')[-1]
            return {'uuid': uuid, 'nick': nick}
        except AttributeError:
            raise Exception("Invalid Blog")

    def get_liker_list(self, soup: BeautifulSoup):
        try:
            res = []
            div = soup.find('div', {'class': 'user-list'})
            links = div.findAll('a')
            i = 0
            for link in links:
                nick = link.text
                uuid = link['href'].split('/')[-1]
                if i == 0 and uuid == me and nick[-1] == '、':
                    nick = nick[:-1]
                res.append({'uuid': uuid, 'nick': nick})
                i += 1
            return res
        except AttributeError:
            raise Exception("Invalid Blog")

    def get_commenter_list(self, soup: BeautifulSoup):
        pass
    