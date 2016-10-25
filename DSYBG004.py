#coding:utf-8
import requests
import re
import os
import string
from lxml import etree

isProxyNeeded = False


class AllData:
    def __init__(self):
        self.m_weixins = []

    def add_weixin(self, weixin):
        self.m_weixins.append(weixin)

    def html_transform(self, line):
        line = line.replace('amp;', '')
        line = line.replace('&quot;', '"')
        line = line.replace('&#39;', "'")
        line = line.replace('&gt;', '>')
        line = line.replace('&lt;', '<')
        line = line.replace('&yen;', '¥')
        line = line.replace('\\\/', '/')
        return line

class Weixin:
    def __init__(self, name= "", address = ""):
        self.m_name = name
        self.m_address = address
        self.m_topics = {}

    def setName(self, name):
        self.m_name = name

    def setAddress(self, address):
        self.m_address = address

    def addTopic(self, key, topic):
        self.m_topics[key] = topic

class Topic:
    def __init__(self, name, address):
        self.m_name = name
        self.m_address = address
        self.m_topic = []

    def setName(self, name):
        self.m_name = name

    def setAddress(self, address):
        self.m_address = address

    def setTopic(self, topic):
        self.m_topic = topic

class NetWorkSetting:
    def __init__(self):
        self.proxy = {
            "http": 'http://10.144.1.10:8080',
            "https": 'https://10.144.1.10:8080'}
        self.searchUrl = 'http://weixin.sogou.com/weixin?type=1&query='
        self.prefixUrl = 'http://mp.weixin.qq.com'
        self.searchKey = "python"
        self.myHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://weixin.sogou.com/weixin?type=1&query='
}

#1. get result for key word search
print "1, get result for key word search"
wmp = AllData()
setting = NetWorkSetting()
setting.searchKey = "python"
session = requests.Session()
target_url = setting.searchUrl + setting.searchKey

if isProxyNeeded:
    result = session.get(target_url, headers=setting.myHeaders, proxies=setting.proxy)
else:
    result = session.get(target_url, headers=setting.myHeaders)
print result.url, result.status_code

temp = result.content
page = etree.HTML(temp.decode('utf-8'))
address = page.xpath(u"//div[@target='_blank']")
wname = page.xpath(u"//label[@name='em_weixinhao']")

if len(address) == len(wname):
    for i in range(0,len(address)):
        eachweixin = Weixin()
        #find the weixin address
        line = str(address[i].attrib)
        index = line.find("gotourl(")
        if -1 == index:
            continue
        else:
            line = line[index + 9:]
            index = line.find("'")
            line = line[0:index]
            line = wmp.html_transform(line)
            eachweixin.setAddress(line)
        #find the weixin name
        eachweixin.setName(wname[i].text)
        wmp.m_weixins.append(eachweixin)
else:
    print "error happen in weixinhao!!"
    pass

#2. for all weixinhao exist in glable data, get the source and get all the topics for each weixinhao, then write to glable data
print "2, for all weixinhao exist in glable data, get the source and get all the topics for each weixinhao, then write to glable data"
tempindex = 1
for weixin in wmp.m_weixins:
    setting.myHeaders['Referer'] = setting.searchUrl + weixin.m_name
    target_url = weixin.m_address
    if isProxyNeeded:
        result = session.get(target_url, headers=setting.myHeaders, proxies=setting.proxy)
    else:
        result = session.get(target_url, headers=setting.myHeaders)
    tempfilename = "temp/" + str(i) + ".txt"
    i += 1
    f = open(tempfilename,'w+')
    f.write(result.content)
    f.close()

    #parse the source and get all the topic's url in one string
    f = open(tempfilename, "r")
    lines = f.readlines()
    topics_url = ''
    for line in lines:
        current = line.find("msgList")
        if -1 == current:
           continue
        else:
            line = line.replace('amp;', '')
            line = line.replace('&quot;', '"')
            line = line.replace('&#39;', "'")
            line = line.replace('&gt;', '>')
            line = line.replace('&lt;', '<')
            line = line.replace('&yen;', '¥')
            line = line.replace('\\\/', '/')
            topics_url = line
            print "topics_url"
            print topics_url

    #get each topic's url and save it in wmp's data
    current = 0
    print weixin.m_topics
    #todo
    topicIndex = 0
    while current != -1:
        current = topics_url.find("content_url")
        if current == -1:
            break
        topics_url = topics_url[current + 14:]
        current = topics_url.find("source_url")
        if current == -1:
            break
        print topics_url[0:current - 3]
        weixin.m_topics[topicIndex] = setting.prefixUrl + topics_url[0:current - 3]
        topicIndex += 1
        topics_url = topics_url[current:]
    print weixin.m_topics


#3 start to scrapy real topic for every weixinhao
print "3, start to scrapy real topic for every weixinhao"
for weixin in wmp.m_weixins:
    tempPath = "target\\" + weixin.m_name
    if os.path.exists(tempPath):
        pass
    else:
        os.makedirs(tempPath)
    #print weixin.m_topics
    index = 0
    for topic in weixin.m_topics.values():
        print "topic: "
        print topic
        if isProxyNeeded:
            result = session.get(topic, headers=setting.myHeaders, proxies=setting.proxy)
        else:
            result = session.get(topic, headers=setting.myHeaders)
        topicfile = tempPath +"\\" + str(index) + ".html"
        index += 1
        f = open(topicfile, 'w+')
        f.write(result.content)
        f.flush()
        f.close()


print "end of now"



