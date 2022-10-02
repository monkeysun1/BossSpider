# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:36:10 2022

@author: Administrator
openpyxl
"""
import json,time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd



#打开网站（手动扫码登录、保存Cookie）
def SaveCookie():
    browser.get('https://www.zhipin.com/')
    input('请手动登录网站，按回车键继续……')
    cookies = browser.get_cookies()
    with open('BossCookie.txt','w') as f:
        json.dump(cookies, f)
        print('cookie已保存。')
#读取Cookie并登录
def CookieLogin():
    browser.get('https://www.zhipin.com')
    time.sleep(10)
    f = open('BossCookie.txt','r')
    cookies = json.load(f)
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.refresh()
#通过搜索链接获取详情链接
searchUrl = 'https://www.zhipin.com/web/geek/job?query=%E6%95%B0%E6%8D%AE%2F%E7%AD%96%E7%95%A5%E8%BF%90%E8%90%A5&city=100010000'
def GetDetailUrls(searchUrl):
    browser.get(searchUrl)
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html,'lxml')
    detailList = soup.find_all('a',class_='job-card-left')
    detailList = ['https://www.zhipin.com'+i.get('href') for i in detailList]
    return detailList
#通过详情链接获取职位信息
def detailData(detailUrl):
    browser.get(detailUrl)
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html,'lxml')
    #职位
    try:
        zhiwei = soup.h1['title']
    except:
        print('职位获取失败，尝试刷新……')
        browser.refresh()
        time.sleep(20)
        html = browser.page_source
        soup = BeautifulSoup(html,'lxml')
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
#生成搜索链接
def getSearchUrls(jobs,city,pages):
    SearchUrlList = []
    for job in jobs:
        for page in range(pages):
            SearchUrl = 'https://www.zhipin.com/web/geek/job?query=%s&city=%s&page=%s'%(job,city,page+1)
            SearchUrlList.append(SearchUrl)
    return SearchUrlList
b = input('1:保存cookie，其它:运行爬虫\n：')
if b=='1':
    SaveCookie()
else:
    jobs = ['数据','统计','excel','运营'] #搜索关键词
    city = 101220200 #城市代码
    pages = 10 #共抓取几页
    #生成df
    df = pd.DataFrame()
    #打开浏览器
    browser = webdriver.Chrome()
    #登录
    CookieLogin()
    #搜索
    SearchUrlList = getSearchUrls(jobs,city,pages)
    for SearchUrl in SearchUrlList:
        print('解析搜索链接……')   
        detailList = GetDetailUrls(SearchUrl)
        for detailUrl in detailList:
            print('解析详情链接……')
            try:
                data = detailData(detailUrl)
            except:
                print('跳过……')
                continue
            df = df.append(data, ignore_index = True)
    df.to_excel('boss.xlsx')
    browser.quit()
