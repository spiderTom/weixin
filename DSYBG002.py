#coding:utf-8
import requests
import re
import string


http_proxy = {"http": 'http://10.144.1.10:8080',
              "https": 'https://10.144.1.10:8080'}
search_url = 'http://weixin.sogou.com/weixin?type=1&query='
public_url = ''
prefix_url = 'http://mp.weixin.qq.com'

my_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Referer': 'http://weixin.sogou.com/weixin?type=1&query='
}

sss = requests.Session()
target_url = search_url + "python_friend"
print target_url
r = sss.get(target_url, headers=my_headers, proxies=http_proxy)
#r = sss.get(target_url, headers=my_headers)
print r.url, r.status_code, r.history
f = open('test.html','w+')
f.write(r.content)
f.close()

f = open("test.html", "r")
lines = f.readlines()
for line in lines:
    current = line.find("gotourl(")
    if -1 == current:
        continue
    else:
        line = line[current + 9:]
        current = line.find("'")
        line = line[0:current]
        line = line.replace('amp;', '')
        public_url = line

my_headers['Referer'] = search_url + "python_friend"
r = sss.get(public_url, headers=my_headers, proxies=http_proxy)
#r = sss.get(public_url, headers=my_headers)
print r.url, r.status_code, r.history
f = open('test2.html','w+')
f.write(r.content)
f.close()


f = open("test2.html", "r")
lines = f.readlines()
target_url = ""
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
        target_url = line
        print target_url
names = []
current = 0
i = 0
while current != -1:
    current = target_url.find("content_url")
    if current == -1:
        break
    target_url = target_url[current + 14:]
    current = target_url.find("source_url")
    if current == -1:
        break
    names.append(target_url[0:current - 3])
    target_url = target_url[current:]
    i += 1

i = 0
for item in names:
    item = prefix_url + item
    print item
    r = sss.get(item, headers=my_headers, proxies=http_proxy)
    filename = str(i) + ".html"
    print "filename: " + filename
    f = open(filename,'w+')
    f.write(r.content)
    f.close()
    i += 1
