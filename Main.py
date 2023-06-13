# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 11:01:00 2022

@author: Administrator
"""
import json, time, random
from concurrent.futures import ThreadPoolExecutor
import logging
from logging.handlers import RotatingFileHandler

from selenium.common.exceptions import WebDriverException

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

class UrlQuery:
    query = '爬虫'  # 搜索关键词
    city = 100010000  # 城市代码，默认蚌埠     全国 ： 100010000  西安 ：101110100
    degree = ''  # 学历要求 硕士：204  本科：203  博士：205
    industry = ''  # 公司行业
    experience = ''  # 工作经验
    position = ''  # 职业类型
    salary = 406  # 薪资待遇，默认5~10K  10-20K：405  20-50k:406 50k以上：407
    scale = ''  # 公司规模
    stage = ''  # 融资阶段

proxypool_url = 'http://127.0.0.1:5555/random'

def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()


#构建链接

def get_recommend_url():
    query_url = 'https://www.zhipin.com/web/geek/recommend?ka=open_joblist&sortType=2'
    return query_url

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

def get_child_page(browser, base_url):
    urls =[]
    num = 0
    browser.get(base_url)
    while True:
        Current_url = browser.current_url
        urls.append(Current_url)
        num += 1
        print(Current_url)
        browser.find_element_by_css_selector("[class='ui-icon-arrow-right']").click()
        NewUrl = browser.current_url
        if Current_url == NewUrl:
            break
    return urls, num


def get_boss_data(query : UrlQuery, logger):
    df = pd.DataFrame()  # 生成df

    while True:
        proxy = get_random_proxy()
        print(proxy)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--proxy-server=http://" + proxy)
        browser = webdriver.Chrome(options=options)
        browser.implicitly_wait(20)
        browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        # browser.maximize_window()
        try:
            browser.get('https://www.zhipin.com')
            time.sleep(15)
        except WebDriverException:
            continue
        logger.debug('IP:%s, page: %s ',proxy, browser.page_source)

        if browser.page_source.find('无法访问此网站') == -1:
            break
        logger.debug("IP:%s not avaiable",proxy)



    print('如需验证人工，请手动验证。')
    a = input('1.登录保存Cookie，2.Cookie登录，其它.不登录直接抓取：')
    if a == '1':
        SaveCookie(browser)
    elif a == '2':
        CookieLogin(browser)
    else:
        pass

    base_url = get_url(query)
    #base_url = get_recommend_url()
    browser.get(base_url)

    time.sleep(25)
    # urls, num = get_child_page(browser , base_url)
    # print(num, urls)
    timeDelay = random.randint(10, 20)  # 每次打开网页延迟时间  # 每次打开网页延迟时间
    page_num = 0
    contine_num_zero = 0
    # while True:
    #     if page_num >= num:
    #         break
    #     browser.get(urls[page_num % num])
    #     btns = browser.find_elements_by_css_selector("[class='job-name']")
    #     Current_url = browser.current_url
    #     print(Current_url)
    #     num = len(btns)
    #     print('当前页获取%s条招聘信息……' % num)
    #     if num == 0:
    #         contine_num_zero += 1
    #         if(contine_num_zero > 3):
    #             browser.get(urls[page_num % num])
    #         time.sleep(25)
    #         continue
    #         # try:
    #         #     print('进入下一页')
    #         #     browser.find_element_by_css_selector("[class='ui-icon-arrow-right']").click()
    #         #     time.sleep(timeDelay)
    #         #     NewUrl = browser.current_url
    #         #     if Current_url == NewUrl:
    #         #         print('已至最后一页，结束运行……')
    #         #         break
    #         #     time.sleep(timeDelay)
    #         # except Exception as e:
    #         #     print(e)
    #         #     browser.refresh()
    #     contine_num_zero = 0
    #     page_num += 1
    #     for btn in btns:
    #         try:
    #             btn.click()  # 进入详情页
    #         except:
    #             continue
    #         time.sleep(timeDelay)
    #         allWindows = browser.window_handles
    #         browser.switch_to.window(allWindows[1])
    #         try:
    #             print('尝试获取详情信息')
    #             data = detailData(browser)
    #             df = df.append(data, ignore_index=True)
    #         except:
    #             print('信息获取失败，跳过……')
    #             time.sleep(timeDelay * 2)
    #         browser.close()
    #         browser.switch_to.window(allWindows[0])
    while True:
        btns = browser.find_elements_by_css_selector("[class='job-name']")
        Current_url = browser.current_url
        print(Current_url)
        num = len(btns)
        print('当前页获取%s条招聘信息……' % num)
        if num == 0:
            time.sleep(25)
            browser.get(Current_url)
            continue
            # try:
            #     print('进入下一页')
            #     browser.find_element_by_css_selector("[class='ui-icon-arrow-right']").click()
            #     time.sleep(timeDelay)
            #     NewUrl = browser.current_url
            #     if Current_url == NewUrl:
            #         print('已至最后一页，结束运行……')
            #         break
            #     time.sleep(timeDelay)
            # except Exception as e:
            #     print(e)
            #     browser.refresh()

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
                time.sleep(timeDelay*2)
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
            time.sleep(timeDelay)
        except Exception as e:
            print(e)
            browser.refresh()

    fileName = time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(time.time()))
    fileName = "query:" + query.query + fileName
    df.to_excel('%s.xlsx' % fileName)
    browser.quit()


def test_proxy():
    proxy = get_random_proxy()
    print(proxy)
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=http://" + proxy)  #
    browser = webdriver.Chrome(options=options)
    browser.get('https:/www.httpbin.org/get')
    print(browser.page_source)


def multi_Tread_scrapy(logger):
    ele_list = []
    query1 = UrlQuery()
    query1.query = 'C%2B%2B'
    query1.city = 101110100
    ele_list.append(query1)

    query2 = UrlQuery()
    query2.query = 'python'
    query2.city = 101110100
    ele_list.append(query2)

    query3 = UrlQuery()
    query3.query = 'django'
    query3.city = 100010000
    ele_list.append(query3)

    pool = ThreadPoolExecutor(max_workers=len(ele_list))
    # 向线程池提交一个task, 50会作为action()
    for query in ele_list:
        future1 = pool.submit(get_boss_data, query,logger)
    pool.shutdown(wait=True)

if __name__== '__main__':

    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    f_handler = RotatingFileHandler('debug.log', maxBytes=10 * 1024 * 1024, backupCount=5)
    # f_handler = logging.FileHandler('debug.log')
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
    logger.addHandler(f_handler)
    query = UrlQuery()
    #get_boss_data(query,logger)
    #test_proxy()
    multi_Tread_scrapy(logger)