# python
# -*- coding:utf8 -*-
# Create by 张亚杰 on 2016/4/4

import urllib
import urllib2
import re
import os


#百度贴吧爬虫类
class BDTB:

    #初始化，传入基地址
    def __init__(self,baseUrl):
        self.baseURL = baseUrl
        self.x =0

    #传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            url = self.baseURL + '?pn=' + str(pageNum)
            print url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
                return None

    #获取帖子标题
    def getTitle(self,page):
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
        result = re.search(pattern,page)
        if result:
            #print result.group(1)  #测试输出
            return result.group(1).strip()
        else:
            pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
            result = re.search(pattern, page)
            if result:
                print result.group(1)  # 测试输出
                return result.group(1).strip()
            else:
                return None

    #获取帖子一共有多少页
    def getPageNum(self,page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span .*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)

        if result:
            #print result.group(1)  #测试输出
            return result.group(1).strip()
        else:
            return None

     # 获取帖子内的图片并存储到D:/ImageDownload
    def getImg(self, page,title):
        # reg = r'class="BDE_Image" src="(.+?)\.jpg" pic_ext'
        # imgre = re.compile(reg)
        picpath = 'D:\\ImageDownload\\%s' % (title)
        if not os.path.exists(picpath):  # 路径不存在时创建一个
            os.makedirs(picpath)
        imglist = re.findall('class="BDE_Image" src="(.+?)"',page,re.S)
        self.x
        for imgurl in imglist:
            #local = 'F:\\img\\'
            urllib.urlretrieve(imgurl, picpath + '\\%s.jpg' % self.x)
            self.x +=1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)      #贴吧标题
       # self.setFileTitle(title)
        if pageNum == None:
            print "URL已失效，请重试"
            return
        try:
            print "该帖子共有" + str(pageNum) + "页"
            for i in range(1,int(pageNum)+1):
                print "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getImg(page,title)
        #出现写入异常
        except IOError,e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成！！！！"


baseURL = 'http://tieba.baidu.com/p/4405041388'
bdtb = BDTB(baseURL)
bdtb.start()
