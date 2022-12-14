# 说明

参数：

```python
query = '' #搜索关键词
city = 101220200 #城市代码，默认蚌埠
degree = '' #学历要求
industry = '' #公司行业
experience = '' #工作经验
position = '' #职业类型
salary = 404  #薪资待遇，默认5~10K
scale = '' #公司规模
stage = ''#融资阶段
timeDelay = 20 #每次打开网页延迟时间，数值太小可能网页加载不全导致抓取失败，请求速度太快导致被封。
```

城市代码(city)见：https://www.zhipin.com/wapi/zpCommon/data/cityGroup.json

工作经验（experience）、薪资待遇（salary）、融资阶段（stage）、公司规模（scale）、学历（degree）代码见：https://www.zhipin.com/wapi/zpgeek/search/job/condition.json

公司行业（industry）代码见：https://www.zhipin.com/wapi/zpCommon/data/industry.json

职业类型（position）代码见：https://www.zhipin.com/wapi/zpCommon/data/position.json



### 一、前置：

1. 安装Chrome。

2. 下载[chromedriver](https://chromedriver.chromium.org/downloads) 并配置环境变量，网盘备份：https://fuwenyue.lanzouy.com/ittRu0ck7gub 。
3. `pip install -r requirements.txt`

### 二、运行代码：

运行代码有**保存cookie**和**运行爬虫**两个选项：

- 保存Cookie，运行后生成`BossCookie.txt`文件。

自动打开网站，**手动登录**。确认后自动保存Cookie。

- 运行爬虫

自动Cookie登录，根据配置运行代码。

```python
    jobs = ['数据','统计','excel','运营'] #搜索关键词
    city = 101220200 #城市代码
    pages = 10 #共抓取几页
```

运行完毕后生成个`.xlsx`文件。

![](https://pan.bizha.top/view.php/426098e5bfdd4e83aba87b066811db25.png)
