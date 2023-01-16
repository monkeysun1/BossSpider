# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 08:27:37 2023

@author: Administrator

"""

import pandas as pd
import glob,os

all_describeList = pd.DataFrame()

floder = r'C:\Users\Administrator\OneDrive\桌面\MyCode\BossZhipin'
fileList = glob.glob(os.path.join(floder,'*.xlsx'))


#读取所有excel文件
floder = r'C:\Users\Administrator\OneDrive\桌面\MyCode\BossZhipin'
fileList = glob.glob(os.path.join(floder,'*.xlsx'))
if 'All' in fileList[-1]:
    print('删除All.xlsx')
    all_describeList = pd.read_excel(fileList[-1],sheet_name=0)
    fileList = glob.glob(os.path.join(floder,'*.xlsx'))[:-1]

#fileList
for fileName in fileList:
    print('正在读取:%s'%fileName)
    DF_zhiwei = pd.read_excel(fileName,sheet_name=0)
    date = fileName.split('\\')[-1]
    date = date.split('.')[0]
    DF_zhiwei['抓取日期'] = date
    all_describeList = pd.concat([all_describeList,DF_zhiwei],axis=0)

all_describeList.drop_duplicates(subset=['职位描述'], keep='first', inplace=True, ignore_index=False)
#all_describeList = all_describeList.reset_index(drop=True)  
all_describeList.drop(columns = 'Unnamed: 0', inplace=True) #删除第一列
all_describeList.to_excel('All.xlsx',index=False)
