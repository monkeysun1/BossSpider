# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 11:01:00 2022

@author: Administrator
"""
import json,time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

query = '' #搜索关键词
city = 101220200 #城市代码，默认蚌埠
degree = '' #学历要求
industry = '' #公司行业
experience = '' #工作经验
position = '' #职业类型
salary = 404  #薪资待遇，默认5~10K
scale = '' #公司规模
stage = ''#融资阶段

#构建链接
baseUrl = 'https://www.zhipin.com/web/geek/job?'
if query != '':
    baseUrl = baseUrl+'query=%s&'%query
if city != '':
    baseUrl = baseUrl+'city=%s&'%city
if degree != '':
    baseUrl = baseUrl+'degree=%s&'%degree
if industry != '':
    baseUrl = baseUrl+'industry=%s&'%industry
if experience !='' :   
    baseUrl = baseUrl+'experience=%s&'%experience
if position  !='' : 
    baseUrl = baseUrl+'position=%s&'%position
if salary != '':
    baseUrl = baseUrl+'salary=%s&'%salary  
if scale != '':
    baseUrl = baseUrl+'scale=%s&'%scale
if stage != '':
     baseUrl = baseUrl+'stage=%s&'%stage
if baseUrl[-1] == '&':
    baseUrl = baseUrl[:-1]

#打开网站（手动扫码登录、保存Cookie）
def SaveCookie(browser):
    browser.get('https://www.zhipin.com/')
    input('请手动登录网站，按回车键继续……')
    cookies = browser.get_cookies()
    with open('BossCookie.txt','w') as f:
        json.dump(cookies, f)
        print('cookie已保存。')
#读取Cookie并登录
def CookieLogin(browser):
    browser.get('https://www.zhipin.com')
    time.sleep(10)
    f = open('BossCookie.txt','r')
    cookies = json.load(f)
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.refresh()
#    time.sleep(10)
#解析详情页
def detailData(browser):
    soup = BeautifulSoup(browser.page_source,'lxml')
    zhiwei = soup.h1['title']
    #薪水
    xinshui = soup.find('span',class_="salary").get_text()
    #公司名称
    try:
        gongsi = soup.find('li',class_="company-name").get_text()
    except:
        try:
            gongsi = soup.find('a',ka="job-detail-company_custompage").get_text()
        except:
            gongsi = 'gongsi'
        
    gongsi = gongsi.replace('公司名称','')
    #公司地址
    try:
        dizhi = soup.find('div',class_="location-address").get_text()
    except:
        dizhi = 'dizhi'
    #人事
    renshi = soup.h2.get_text()
    name = renshi.split('\n')[0]
    try:
        lastlogin = renshi.split('\n')[1]
    except:
        lastlogin = 'lastlogin'
    #学历
    xueli = soup.find('span',class_="text-desc text-degree").get_text()
    #职位描述
    miaosu = soup.find('div',class_="job-sec-text").get_text()
    data = {'公司名称':gongsi,'职位':zhiwei,'薪水':xinshui,'学历要求':xueli,'职位描述':miaosu,'人事':name,'上次活跃':lastlogin,'地址':dizhi,'链接':browser.current_url}
    return data

df = pd.DataFrame() #生成df
browser = webdriver.Chrome() 
browser.maximize_window() 
#CookieLogin(browser)
browser.get(baseUrl)
time.sleep(10)
while True:
    btns = browser.find_elements_by_css_selector("[class='job-name']")
    print('当前页获取%s条招聘信息……'%len(btns))
    for btn in btns :
        btn.click() #进入详情页
        time.sleep(10)
        allWindows = browser.window_handles
        browser.switch_to.window(allWindows[1])
        try:
            print('尝试获取详情信息')
            data = detailData(browser)
            df = df.append(data, ignore_index = True)
            print('√')
        except:
            print('信息获取失败，跳过……')
#        allWindows = browser.window_handles
#        browser.switch_to.window(allWindows[1])
        browser.close()
        browser.switch_to.window(allWindows[0])
        
    try:
        print('尝试翻页')
        browser.find_element_by_css_selector("[class='ui-icon-arrow-right']").click()
        time.sleep(10)
    except:
        break

df.to_excel('boss.xlsx')
browser.quit()

