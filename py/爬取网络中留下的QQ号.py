import urllib.request
import ssl
import re
from collections import deque
#QQ群：592857363
def writeFileBytes(htmlBytes,toPath):
    with open(toPath,"wb") as f:
        f.write(htmlBytes)
def writeFileStr(htmlBytes,toPath):
    with open(toPath,"w") as f:
        f.write(str(htmlBytes))
def getHtmlBytes(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(req, context=context)
    return response.read()
def qqCrawler(url,toPath):
    htmlBytes = getHtmlBytes(url)
    htmlStr = str(htmlBytes)
    pat = r'(((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?)'
    re_url = re.compile(pat)
    urlList = re_url.findall(htmlStr)
    urlList = list(set(urlList))
    pat = "[1-9]\d{4,9}"
    re_qq = re.compile(pat)
    qqsList = re_qq.findall(htmlStr)
    qqsList = list(set(qqsList))
    f = open(toPath,"a")
    for qqStr in qqsList:
        f.write(qqStr + "\n")
    f.close()
    return urlList

def center(url, toPath):
    queue = deque()
    queue.append(url)
    while len(queue) != 0:
        targetUrl = queue.popleft()
        urlList = qqCrawler(targetUrl, toPath)
        for item in urlList:
            tempUrl = item[0]
            queue.append(tempUrl)

url = "https://www.douban.com/group/topic/92896862/"
toPath = r"F:\QQDoc\qqFile.txt"
center(url, toPath)






