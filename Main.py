import requests
from lxml import html
import clipboard
import copy
import re

from wox import Wox

import os
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'ShortUrl.log'),
    filemode='w+'
)

result_template = {
    'Title': '{}',
    'SubTitle': 'Press enter copy magnet url',
    'IcoPath': 'img/app.png',
    'JsonRPCAction': {
        'method': 'copytoclipboard',
        'parameters': ['{}'],
    }
}

class Main(Wox):

    def query(self, param):
        results = []
        q = param.strip()
        if not q:
            results.append({
            "Title": "新浪短链",
            "SubTitle": "Get short url",
            "IcoPath":"img/app.png",
            "ContextData": "ctxData"
            })
            return results
           
        if q[0:4] != "http":
            q = "http://" + q
        
        if not re.match(r"^(http://){0,1}[A-Za-z0-9][A-Za-z0-9\-\.]+[A-Za-z0-9]\.[A-Za-z]{2,}[\43-\176]*$",q):
            results.append({
            "Title": "新浪短链",
            "SubTitle": "LongUrl: %s" % q,
            "IcoPath":"img/app.png",
            "ContextData": "ctxData"
            })
            return results
            
        response = self.getshorturl(q)
        if not response:
            results.append({
            "Title": "新浪短链",
            "SubTitle": "Get short url failed",
            "IcoPath":"img/app.png",
            "ContextData": "ctxData"
            })
            return results
        
        results.append({
            "Title": "新浪短链",
            "SubTitle": "ShortUrl: %s" % response,
            "IcoPath":"img/app.png",
            "JsonRPCAction": {
                'method': 'copytoclipboard',
                'parameters': [response],
            }
            })
            
        return results
            
            
    def copytoclipboard(self, value):
        clipboard.copy(value)

    @staticmethod
    def getshorturl(url):
        api_url = "http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=" + url
        s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        res = s.get(api_url, headers=headers)
        if res.ok:
            resultData = res.content.decode('utf-8')
            dictData = eval(resultData)
            short_url = dictData[0]['url_short']
            return short_url
        else:
            return ""

    def __get_proxies(self):
        proxies = {}
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies["http"] = "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))
            proxies["https"] = "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))
        return proxies


if __name__ == '__main__':
    Main()
