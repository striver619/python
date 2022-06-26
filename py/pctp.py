import requests

url ='https://www.duitang.com/napi/blog/list/by_search/?kw=%E8%B5%B5%E4%B8%BD%E9%A2%96&start={}&limit=1000' 

pages=[]
for a in range(0,3600,100):
    url_2 = url.format(a)
    html = requests.get(url_2).content.decode('utf-8')
    pages.append(html)

bengin='"path":"'
end1='"'
for b in pages:
    end = 0
    while b.find(bengin,end)!=-1:
        start = b.find(bengin,end)+len(bengin)
        end = b.find(end1,start)
        url_img = b[start:end]
        print(url_img) 
