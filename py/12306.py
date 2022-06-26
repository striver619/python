#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
通过splinter刷12306火车票
可以自动填充账号密码，同时，在登录时，也可以修改账号密码
然后手动识别验证码，并登陆，接下来的事情，交由脚本来做了，静静的等待抢票结果就好（刷票过程中，浏览器不可关闭）
"""
import re
from splinter.browser import Browser
from time import sleep
import time
import sys
import httplib2
from urllib import parse
import smtplib
import numpy as np
from email.mime.text import MIMEText
class BrushTicket(object):
    """买票类及实现方法"""
    def __init__(self, user_name, password, passengers, from_time, from_station, to_station, number, seat_type):
        """定义实例属性，初始化"""
        # 1206账号密码
        self.user_name = user_name
        self.password = password
        # 乘客姓名
        self.passengers = passengers
        # 起始站和终点站
        self.from_station = from_station
        self.to_station = to_station
        # 乘车日期
        self.from_time = from_time
        # 车次编号
        self.number = number.capitalize()
        # 座位类型所在td位置
        if seat_type == '商务座特等座':
            seat_type_index = 1
            seat_type_value = 9
        elif seat_type == '一等座':
            seat_type_index = 2
            seat_type_value = 'M'
        elif seat_type == '二等座':
            seat_type_index = 3
            seat_type_value = 0
        elif seat_type == '高级软卧':
            seat_type_index = 4
            seat_type_value = 6
        elif seat_type == '软卧':
            seat_type_index = 5
            seat_type_value = 4
        elif seat_type == '动卧':
            seat_type_index = 6
            seat_type_value = 'F'
        elif seat_type == '硬卧':
            seat_type_index = 7
            seat_type_value = 3
        elif seat_type == '软座':
            seat_type_index = 8
            seat_type_value = 2
        elif seat_type == '硬座':
            seat_type_index = 9
            seat_type_value = 1
        elif seat_type == '无座':
            seat_type_index = 10
            seat_type_value = 1
        elif seat_type == '其他':
            seat_type_index = 11
            seat_type_value = 1
        else:
            seat_type_index = 7
            seat_type_value = 3
        self.seat_type_index = seat_type_index
        self.seat_type_value = seat_type_value

        # 主要页面网址
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.init_my_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        # 浏览器驱动信息，驱动下载页：https://sites.google.com/a/chromium.org/chromedriver/downloads
        self.driver_name = 'chrome'
        self.executable_path = r'C:\Users\redhat\AppData\Local\Programs\Python\Python38\chromedriver.exe'

    def do_login(self):
        """登录功能实现，手动识别验证码进行登录"""
        self.driver.visit(self.login_url)
        sleep(1)
        self.driver.fill('loginUserDTO.user_name', self.user_name)
        self.driver.fill('userDTO.password', self.password)
        print('请输入验证码……')
        while True:
            if self.driver.url != self.init_my_url:
                sleep(1)
            else:
                break

    def start_brush(self):
        """买票功能实现"""
        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        # 浏览器窗口的大小
        self.driver.driver.set_window_size(1000, 900)
        self.do_login()
        self.driver.visit(self.ticket_url)
        try:
            print('开始刷票……')
            # 加载车票查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.from_station})
            self.driver.cookies.add({"_jc_save_toStation": self.to_station})
            self.driver.cookies.add({"_jc_save_fromDate": self.from_time})
            self.driver.reload()
            count = 0
            while self.driver.url.split('?')[0] == self.ticket_url:
                self.driver.find_by_text('查询').click()
                sleep(1)
                count += 1
                print('第%d次点击查询……' % count)
                try:
                    car_no_location = self.driver.find_by_id("queryLeftTable")[0].find_by_text(self.number)[0]
                    current_tr = car_no_location.find_by_xpath("./../../../../..")
                    if current_tr.find_by_tag('td')[self.seat_type_index].text == '--':
                        print('无此座位类型出售，已结束当前刷票，请重新开启！')
                        sys.exit(1)
                    elif current_tr.find_by_tag('td')[self.seat_type_index].text == '无':
                        print('无票，继续尝试……')
                    elif current_tr.find_by_tag('td')[self.seat_type_index].text == '候补':
                        print('候补，继续尝试……')
                    else:
                        # 有票，尝试预订
                        print('刷到票了（余票数：' + str(current_tr.find_by_tag('td')[self.seat_type_index].text) + '），开始尝试预订……')
                        current_tr.find_by_css('td.no-br>a')[0].click()
                        sleep(1)
                        print('开始选择用户……')
                        key_value = 1
                        for p in self.passengers:
                            # 选择用户
                            self.driver.find_by_text(p).last.click()
                            # 选择座位类型
                            seat_select = self.driver.find_by_id("seatType_" + str(key_value))[0]
                            seat_select.find_by_xpath("//option[@value='" + str(self.seat_type_value) + "']")[0].click()
                            key_value += 1
                            sleep(0.5)
                            if p[-1] == ')':
                                self.driver.find_by_id('dialog_xsertcj_ok').click()
                                print('正在提交订单……')
                                self.driver.find_by_id('submitOrder_id').click()
                                sleep(0.5)
                            # 查看放回结果是否正常
                            submit_false_info = self.driver.find_by_id('orderResultInfo_id')[0].text
                            if submit_false_info != '':
                                print(submit_false_info)
                                self.driver.find_by_id('qr_closeTranforDialog_id').click()
                                sleep(0.2)
                                self.driver.find_by_id('preStep_id').click()
                                sleep(0.3)
                                continue
                        print('正在确认订单……')
                        self.driver.find_by_id('submitOrder_id').click()
                        sleep(1)
                        print('预订成功，请及时前往支付……')

                        # 发送内容
                        def mail_to(neirong, biaoti, geishei):
                            text = neirong
                            msg = MIMEText(text, 'plain', 'utf-8')
                            msg['subject'] = biaoti
                            msg["From"] = geishei
                            s = smtplib.SMTP(SMTPServer, 25)
                            s.login(sender, passwd)
                            s.sendmail(sender, sender, msg.as_string())
                            s.quit()
                        mail_to(neirong, biaoti, geishei)

                        #self.driver.quit()
                except Exception as error_info:
                    print(error_info)
                    #self.driver.quit()
                    break
        except Exception as error_info:
            print(error_info)
            self.driver.quit()
            sys.exit(1)

if __name__ == '__main__':
    # 城市cookie字典
    city_list = {
    'bj': '%u5317%u4EAC%2CBJP', # 北京
    'hd': '%u5929%u6D25%2CTJP', # 邯郸
    'nn': '%u5357%u5B81%2CNNZ', # 南宁
    'wh': '%u6B66%u6C49%2CWHN', # 武汉
    'cs': '%u957F%u6C99%2CCSQ', # 长沙
    'ty': '%u592A%u539F%2CTYV', # 太原
    'yc': '%u8FD0%u57CE%2CYNV', # 运城
    'gz': '%u5E7F%u5DDE%2CGZQ', # 广州
    'qhc': '%u6E05%u6CB3%u57CE%2CQYP' # 清河城
    }
    #邮件信息
    SMTPServer = "smtp.163.com"
    sender = "**********@163.com"
    passwd = "********"
    c = time.time()
    b = time.localtime(c)
    q = time.strftime("%Y-%m-%d %X", b)
    neirong = ("12306:" + q + " 搶到票了，轉進時間吧！")
    biaoti = ("一封信 " + q)
    geishei = sender
    # 从txt中获取信息
    with open(r'E:\Oracle\Stock\基金\理财入门\python\ppcode\code\tickets.txt', 'r', encoding='utf-8', errors='ignore') as f:
        info_array = np.genfromtxt(f, dtype=str, delimiter=':')
        account = info_array[0][1]
        password = info_array[1][1]
        from_time = info_array[2][1]
        start = info_array[3][1]
        end = info_array[4][1]
        from_station = city_list[start]
        to_station = city_list[end]
        number = info_array[5][1]
        seat_type = info_array[6][1]
        passengers = info_array[7][1].split(",")
        #打印购票人信息
        print(account, password, passengers, from_time, from_station, to_station, number, seat_type)
        # 开始抢票
        ticket = BrushTicket(account, password, passengers, from_time, from_station, to_station, number, seat_type)
        ticket.start_brush()

