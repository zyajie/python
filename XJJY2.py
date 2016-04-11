# python
# -*- coding:utf8 -*-
import urllib2
import urllib
import cookielib
from lxml import etree
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def renrenBrower(url,page):
    #登陆页面，可以通过抓包工具分析获得，如fiddler，wireshark
    login_page = "https://passport.jiayuan.com/dologin.php?pre_url=http://usercp.jiayuan.com/"
    url = url + str(page)
    try:
        #获得一个cookieJar实例

        cj = cookielib.CookieJar()
        #cookieJar作为参数，获得一个opener的实例
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #伪装成一个正常的浏览器，避免有些web服务器拒绝访问。
        opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        #生成Post数据，含有登陆用户名密码。
        data = urllib.urlencode({'name':'two_sided_matching@163.com',
        'password':'zxcasdqwe123'})
        #以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
        opener.open(login_page,data)
        #以带cookie的方式访问页面
        op=opener.open(url)
        #读取页面源码
        data= op.read()
        # print data
        while page<151036763:
            pattern2 = re.compile('<li class="cur">.*>(.+?)</a></li>')
            XB = re.search(pattern2, data)  # 资料，查询性别
            pattern = re.compile('<h6 class="member_name">(.+?)</h6>', re.S)
            NL = re.search(pattern, data)  # 年龄和居住地
            selector = etree.HTML(data)
            ID = selector.xpath('//div[@class="member_info_r yh"]/h4/span/text()')[0].replace('ID:', '')  # id
            userInfo = u' '
            userInfo = userInfo + XB.group(1) + u':' + NL.group(1) + u',ID：' + ID
            # 获取基本资料
            list = selector.xpath('//ul[@class="member_info_list fn-clear"]/li/div[@class="fl pr"]/em/text()')
            for each in list:
                # print each
                userInfo = userInfo + u',' + each
            # 获取择偶要求
            list = selector.xpath('//ul[@class="js_list fn-clear"]/li/div/text()')
            for each in list:
                # print each
                userInfo = userInfo + u',' + each
            print(userInfo)
            page += 1
            return data




    except Exception,e:
        print str(e)



url ='http://www.jiayuan.com/'
page =151036758
renrenBrower(url,page)

