# python
# coding=utf8
# Create by zhangyajie on 2016/4/8

import requests
from lxml import etree
import os
import time

# 需要爬取的最大用户数
maxSize = 1000
# 爬虫种子链接，必须为某一个用户页面，用户启动爬虫
seedURL = 'http://www.jiayuan.com/140048773'

# 已经爬取的用户ID，用于后期判断用户信息是否已经存在
visited_ID = []

# 模拟浏览器模式访问服务器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'
}
s = requests.session()

# 模拟登陆状态
def login():
    data = {
        'name':'two_sided_matching@163.com',
        'password':'zxcasdqwe123',
        '_s_x_id':'4eed7264f1e1a795fb47c10fb5eaa0c9',
        'ljg_login':'1',
        'm_p_l':'1',
        'channel':'1',
        'position':'0'
    }
    actoin_url = 'https://passport.jiayuan.com/dologin.php?pre_url=http://usercp.jiayuan.com/'
    s.post(url=actoin_url,data =data,headers=headers)

# 每次程序启动时先清空文件里面已经爬取的数据
f = open('aaa.txt','a')
f.truncate()
f.close()

# 爬虫函数
def getHtml(url):
    f = open('aaa.txt','a')
    headers['Referer'] = url
    response = s.post(url=url, headers=headers)
    selector = etree.HTML(response.text)
    ID = selector.xpath('//div[@class="member_info_r yh"]/h4/span/text()')[0].replace('ID:', '')
    # print('ID：'+ID)
    # 如果这个ID没有爬取过，则进行爬取相应信息
    if ID not in visited_ID:
        # 将此ID加入已访问ID列表中
        visited_ID.append(ID)
        # 将用户信息拼接成一个字符串进行打印
        userInfo = u' '
        userInfo = userInfo + u'ID：' + ID
        # 获取基本资料
        list = selector.xpath('//ul[@class="member_info_list fn-clear"]/li/div[@class="fl pr"]/em/text()')
        for each in list:
            # print each
            userInfo = userInfo + u' ' + each
        # 获取择偶要求
        list = selector.xpath('//ul[@class="js_list fn-clear"]/li/div/text()')
        for each in list:
            # print each
            userInfo = userInfo + u' ' + each
        print(userInfo)
        f.write(userInfo.encode('utf8')+'\r')
        f.close()
    else:
        login()

    # 下一个人的访问连接
    next_url = 'http://www.jiayuan.com/' + ID + '?n=1'

    # 设置睡眠时间，即相邻两次爬取间隔时间
    time.sleep(5)

    # 如果爬取数据达到要求，则程序终止，否则继续
    if (visited_ID.__len__() <= maxSize):
        respone = s.post(url=next_url, headers=headers, allow_redirects=False)
        redirects_url = respone.headers['location']
        # print(response.status_code)
        # print(redirects_url)
        getHtml(redirects_url)
    else:
        os._exit(0)

login()
# 爬虫入口
getHtml(seedURL)
