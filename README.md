# python
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
            'Cookie': r's='XXXX'  } #填入Cookie
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
