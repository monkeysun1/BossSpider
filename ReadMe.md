# 说明

BOSS直聘职位抓取的零碎代码，失败记录见：https://bizha.top/post/bosszhipinone.html ，有其它解决方案请提交issues。

一直抓取失败，最终选择的是`selenium` 获取 html 代码，BeautifulSoup 解析。

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
