# DD-Emblem

## 简介

本项目是一个基于异步框架 aiohttp 来对 Bilibili 的直播间进行抽奖信息监测和领取的小工具，可以用于自动升级粉丝勋章亲密度。

利用模块提供的接口，只需几秒就可以领取哔哩哔哩全站所有直播间舰长抽奖的亲密度，各位可以在此基础上随意拓展。
## 安装项目
首先需要安装第三方依赖。

`$ pip install aiohttp`

接着可以选择安装本项目的包。

`$ pip install ddemblem`.

或是直接下载本项目。

`$ git clone https://github.com/BYOUINZAKA/DD-Emblem.git`

## 使用方法

下载 [Demo.py](https://github.com/BYOUINZAKA/DD-Emblem/blob/master/Demo.py) 。

这段代码展示了一次对于全站直播间抽奖信息的检索和领取，并将领取记录打印出来，其中
```
with open("E:\Python Tools\data\cookies.txt", encoding='utf-8') as cookie:
        headers = Base.createHeaders(UserAgent().firefox, cookie.read())
```
读取了一段cookies文本，这是非常重要的一步。获取请求 Cookie 的方法有很多，这里仅介绍最简单的方法。

打开浏览器登录bilibili后打开开发者模式，刷新B站主页。任找一个带有 Cookie 的请求，最后在 Requests 中复制 Cookie 串即可。

![](http://upload-images.jianshu.io/upload_images/259-0ad0d0bfc1c608b6.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

取得Cookie之后，只需要调用库中提供的API即可使用。
库主要由负责信息检索的 [`Base.Roster`](https://github.com/BYOUINZAKA/DD-Emblem/blob/2e289bfb405748a60e0025704639122812b48c68/DDEmblem/Base.py#L6) 和负责领取奖品的 [`Engine.Receiver`](https://github.com/BYOUINZAKA/DD-Emblem/blob/2e289bfb405748a60e0025704639122812b48c68/DDEmblem/Engine.py#L12) 组成，详细使用方法请参阅 [Demo.py](https://github.com/BYOUINZAKA/DD-Emblem/blob/master/Demo.py)  中的注释。

运行结果：

![](http://upload-images.jianshu.io/upload_images/259-0ad0d0bfc1c608b6.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 作者信息
GitHub：https://github.com/BYOUINZAKA

知乎： https://www.zhihu.com/people/byouinzaka
## 版权信息

该项目签署了 MIT 授权许可，详情请参阅 [LICENSE](https://github.com/BYOUINZAKA/DD-Emblem/blob/master/LICENSE)
