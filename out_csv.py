#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import datetime
import csv
import json

def get_today():
    x = datetime.datetime.now()
    year = str(x.year)
    month = x.month
    date = x.day
    if(month < 10):
        month = "0" + str(month)
    else:
        month = str(month)
    if(date < 10):
        date = "0" + str(date)
    else:
        date = str(date)
    return year + "/" + month + "/" + date + "-00:00:00"

user = input("請輸入帳號:")
password = input("請輸入密碼:")

param = {"cmd" : "login", "id":user ,"password":password}

r = requests.get('https://dinnersystem.com/dinnersys_beta/backend/backend.php', params = param)
if (r.text == "No user" or r.text =="Wrong password" ):
    exit()

cookie = r.cookies["PHPSESSID"]

param = {"cmd" : "select_other", "esti_start":get_today()}
my_cookies = dict(PHPSESSID=cookie)
r = requests.get('https://dinnersystem.com/dinnersys_beta/backend/backend.php', params = param, cookies = my_cookies)
order = r.json()

param = {"cmd" : "show_dish"}
my_cookies = dict(PHPSESSID=cookie)
r = requests.get('https://dinnersystem.com/dinnersys_beta/backend/backend.php', params = param, cookies = my_cookies)
dish = r.json()
dishes = {}

for single in dish:
    dishes[str(single["dish_id"])] = [ single["dish_name"],single["department"]["name"] ]


with open('貼紙.csv', 'w', newline='') as csvfile:

    # 以空白分隔欄位，建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    writer.writerow(['班級座號', '姓名', '餐點','廠商','金額'])
    for person in order:
        now_dish = dishes[person["dish"][0]][0]
        now_department = dishes[person["dish"][0]][1]
        writer.writerow([person["user"]["seat_no"],person["user"]["name"] ,now_dish ,  now_department, person["money"]["charge"]])

print("輸出已完成！")

