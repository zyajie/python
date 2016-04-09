# python
# -*- coding:utf8 -*-
# Create by zhangyajie on 2016/4/8
import urllib
import urllib2
import re
import json
import socket

class XQGP:
    def __init__(self, baseUrl):
        self.baseURL = baseUrl
    def getHtml(self, baseurl, page):
        url=baseurl
        url = baseurl + 'code=SH%s' % page+'&start=0&count=14&_=1460127010224'
        print url
        # Gurl = 'http://xueqiu.com/S/SZ000001'
        send_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'xueqiu.com',
            'Cookie': r's=2rpr13gfjn; _sid=PkaGmJUj8i2SESwZYTeJddETIqfyXN; bid=d1f66c84d79fd726ab0dd3f27c24ba87_imrn9k2u; webp=0; xq_a_token=430758bda2934117ccbac60604cbe43e2e993d2c; xqat=430758bda2934117ccbac60604cbe43e2e993d2c; xq_r_token=02b9d97273a594517aba7241835b2c83d3cfbb98; xq_is_login=1; u=1095623071; xq_token_expire=Tue%20May%2003%202016%2022%3A02%3A02%20GMT%2B0800%20(CST); Hm_lvt_1db88642e346389874251b5a1eded6e3=1460115471,1460123621,1460123653,1460123939; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1460125337; __utma=1.2046135006.1460041599.1460120471.1460122937.4; __utmb=1.14.8.1460125190563; __utmc=1; __utmz=1.1460115472.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        }
        req = urllib2.Request(url, headers=send_headers)
        resp = urllib2.urlopen(req)
        html = resp.read()
        print html
        # decodejson = json.loads(html)
        # print decodejson
        # pattern = re.compile('<a id="followsCount".*?>(.+?)</a>', re.S)
        decodejson = json.loads(html)

        print '股票号：%s,关注度:'%page,decodejson["totalcount"]
        userInfo =  '股票号：'+str(page)+',关注度:' + str(decodejson["totalcount"])
        f = open('XQGP.txt', 'a')
        f.write( userInfo+'\n'+'\r')
        f.close()

    def start(self):
        page =600000
        #超时30秒跳转下一网页
        socket.setdefaulttimeout(30)
        try:
            while page <= 603999:
                html = self.getHtml(self.baseURL,page)
                page += 1
        except:
            page = page + 1
            while page <= 603999:
                html = self.getHtml(self.baseURL, page)
                page += 1


#baseurl='http://xueqiu.com/S'
baseurl='https://xueqiu.com/recommend/pofriends.json?type=1&'

page='600000'
xqgp = XQGP(baseurl)
xqgp.start()
