# encoding=utf-8
import json
import sys
from hdfs import *
import json
import hashlib
import base64
import hmac
import time
import requests
from urllib.parse import quote_plus
from datetime import datetime

timestamp = str(round(time.time() * 1000))
url = 'https://oapi.dingtalk.com/robot/send?access_token={your token}'
secret = '{your secret}'
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = quote_plus(base64.b64encode(hmac_code))

class Send_Message:
    def __init__(self, text):
        self.text = text

    def send_message(self):
        headers = {'Content-Type': 'application/json'}
        webhook = url + '&timestamp=' + timestamp + '&sign=' + sign
        data = {
            "msgtype": "text",
            "text": {
                "content": "%s" % (self.text)
            }
        }
        value = json.dumps(data)
        r = requests.post(webhook, value, headers=headers)
        return r.text

def find_success_file(t, event):
    client = Client("http://bigdata01:50070", "/")
    # file_path = '''/TestLog/test'''
    dir_path = '''/TestDB/%s''' % (event)
    dir_list = client.list(dir_path, status=False)
    dir_name1 = '''DAY=%s''' % (t)
    for dir_name in dir_list:
        if dir_name == dir_name1:
            file_path = '''/TestDB/%s/DAY=%s''' % (event, t)
            file_list = client.list(file_path, status=False)
            for file in file_list:
                print(file)
                if file == "_SUCCESS":
                    return False
    s = Send_Message(event + "事件写出未完成,注意查看！" + "\n通知时间：{}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    s.send_message()
    return True

if __name__ == "__main__":

    yesterday_timestamp = time.time() - 86400
    time_tuple = time.localtime(yesterday_timestamp)
    t = time.strftime("%Y%m%d", time_tuple)
    year = t[0:4]
    year_monthstr = t[0:6]
    year_month_daystr = t
    flag = True
    event = sys.argv[1]
    while flag:
        flag = find_success_file(year_month_daystr, event)
        time.sleep(1)
    print("写出完毕")
    s = Send_Message(event + "写出完毕！" + "\n通知时间：{}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    s.send_message()
    sys.exit(0)
