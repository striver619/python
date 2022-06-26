import requests
import json
import openpyxl
wk = openpyxl.Workbook()
sheet = wk.create_sheet()
resp = requests.get('https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=3725181&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1')
content = resp.text
rest = content.replace('fetchJSON_comment98(','').replace(');','')
json_data = json.loads(rest)
comments = json_data['comments']
for item in comments:
  color = item['productColor']
  size = item['productSize']
  sheet.append([color, size])
  wk.save('data/18910276996.xlsx')




