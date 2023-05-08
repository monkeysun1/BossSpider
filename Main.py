# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 11:01:00 2022

@author: Administrator
"""
import json,time,random
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

class UrlQuery:
    query = ''  # 搜索关键词
    city = 101110100  # 城市代码，默认蚌埠     全国 ： 100010000  西安 ：101110100
    degree = ''  # 学历要求 硕士：204  本科：203  博士：205
    industry = ''  # 公司行业
    experience = ''  # 工作经验
    position = ''  # 职业类型
    salary = 406  # 薪资待遇，默认5~10K  10-20K：405  20-50k:406 50k以上：407
    scale = ''  # 公司规模
    stage = ''  # 融资阶段


#构建链接

def get_url(in_query):
    baseUrl = 'https://www.zhipin.com/web/geek/job?'
    if in_query.query != '':
        baseUrl = baseUrl + 'query=%s&' % in_query.query
    if in_query.city != '':
        baseUrl = baseUrl + 'city=%s&' % in_query.city
    if in_query.degree != '':
        baseUrl = baseUrl + 'degree=%s&' % in_query.degree
    if in_query.industry != '':
        baseUrl = baseUrl + 'industry=%s&' % in_query.industry
    if in_query.experience != '':
        baseUrl = baseUrl + 'experience=%s&' % in_query.experience
    if in_query.position != '':
        baseUrl = baseUrl + 'position=%s&' % in_query.position
    if in_query.salary != '':
        baseUrl = baseUrl + 'salary=%s&' % in_query.salary
    if in_query.scale != '':
        baseUrl = baseUrl + 'scale=%s&' % in_query.scale
    if in_query.stage != '':
        baseUrl = baseUrl + 'stage=%s&' % in_query.stage
    if baseUrl[-1] == '&':
        baseUrl = baseUrl[:-1]
    return baseUrl

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
    f = open('BossCookie.txt','r')
    cookies = json.load(f)
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.refresh()
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
    gongsi = gongsi.replace('\r\n','')
    gongsi = gongsi.replace(' ','')
    print('成功获取 %s 职位……'%gongsi)
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


def get_boss_data():
    df = pd.DataFrame()  # 生成df
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get('https://www.zhipin.com')
    print('如需验证人工，请手动验证。')
    a = input('1.登录保存Cookie，2.Cookie登录，其它.不登录直接抓取：')
    if a == '1':
        SaveCookie(browser)
    elif a == '2':
        CookieLogin(browser)
    else:
        pass
    query = UrlQuery()
    base_url = get_url(query)
    browser.get(base_url)

    timeDelay = random.randint(10,20)  # 每次打开网页延迟时间  # 每次打开网页延迟时间
    while True:
        btns = browser.find_elements_by_css_selector("[class='job-name']")
        Current_url = browser.current_url
        print(Current_url)
        num = len(btns)
        print('当前页获取%s条招聘信息……' % num)
        for btn in btns:
            try:
                btn.click()  # 进入详情页
            except:
                continue
            time.sleep(timeDelay)
            allWindows = browser.window_handles
            browser.switch_to.window(allWindows[1])
            try:
                print('尝试获取详情信息')
                data = detailData(browser)
                df = df.append(data, ignore_index=True)
            except:
                print('信息获取失败，跳过……')
            browser.close()
            browser.switch_to.window(allWindows[0])
        try:
            print('进入下一页')
            browser.find_element_by_css_selector("[class='ui-icon-arrow-right']").click()
            time.sleep(timeDelay)
            NewUrl = browser.current_url
            if Current_url == NewUrl:
                print('已至最后一页，结束运行……')
                break
            time.sleep(timeDelay/10)
        except Exception as e:
            print(e)
            browser.refresh()

    fileName = time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(time.time()))
    fileName = "query:" + UrlQuery.query + fileName
    df.to_excel('%s.xlsx' % fileName)
    browser.quit()


if __name__=='__main__':
    get_boss_data()