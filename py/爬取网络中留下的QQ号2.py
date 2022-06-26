import urllib.request
import ssl
import re
#QQ群：592857363
def getHtmlBytes(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(req, context=context)
    return response.read().decode("utf-8")
def qqCrawler(url,toPath):
    htmlBytes = getHtmlBytes(url)
    htmlStr = str(htmlBytes)
    pat = "[1-9]\d{4,9}"
    re_qq = re.compile(pat)
    qqsList = re_qq.findall(htmlStr)
    qqsList = list(set(qqsList))
    print(qqsList)
    print(len(qqsList))
    f = open(toPath,"a")
    for qqStr in qqsList:
        f.write(qqStr + "\n")
    f.close()
url = "https://www.douban.com/group/topic/92896862/"
toPath = r"F:\QQDoc\qqFile1.txt"
qqCrawler(url,toPath)






