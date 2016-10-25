
import requests
from lxml import etree

root = etree.Element("root")

cs_url = 'https://leetcode.com/articles/remove-nth-node-end-list/'
cs = 'https://github.com/session'
http_proxy = {"https": 'https://10.144.1.10:8080'}
my_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
}
sss = requests.Session()
r = sss.get(cs_url, headers=my_headers, proxies=http_proxy)
print r.url, r.status_code, r.history
#r = sss.post(cs, headers=my_headers, proxies=http_proxy)
#print r.url, r.status_code, r.history
f = open('remove-nth-node-end-list.html','w+')
f.write(r.content)
f.close()
