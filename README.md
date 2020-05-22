<!--
 * @Author: Hata
 * @Date: 2020-03-28 01:08:54
 * @LastEditors: Hata
 * @LastEditTime: 2020-05-22 13:04:30
 * @FilePath: \DD-Emblem\README.md
 * @Description: 
--> 
# DD-Emblem

## 简介

本项目是一个基于异步框架 aiohttp 来对 Bilibili 的直播间进行抽奖信息监测和领取的小工具，可以用于自动升级粉丝勋章亲密度。

利用模块提供的接口，只需几秒就可以领取哔哩哔哩全站所有直播间舰长抽奖的亲密度，可以在此基础上随意拓展。
## 安装项目
首先需要安装第三方依赖。

`$ pip install aiohttp`

接着可以选择安装本项目的包。

`$ pip install ddemblem`

或是直接下载本项目。

`$ git clone https://gitee.com/AnnMaomao/DD-Emblem.git`

## 使用方法

下载 [Demo.py](https://gitee.com/AnnMaomao/DD-Emblem/blob/master/Demo.py) 。


这段代码展示了一次对于全站直播间抽奖信息的检索和领取，并将领取记录打印出来。

其中
```
with open("cookies.txt", encoding='utf-8') as cookie:
        headers = ddemblem.CreateHeaders(cookie.read())
```
读取了一段cookies文本，这是非常重要的一步。获取请求 Cookie 的方法有很多，这里仅介绍最简单的手动方法，如需要也可以自行编写程序获取。

打开浏览器登录bilibili后F12打开开发者模式，刷新B站主页。任找一个带有 Cookie 的请求，最后在 Requests 中复制 Cookie 串，放入cookies.txt即可。

![获取Cookie示例](pic\cookie_exp.png)

取得Cookie之后，只需要调用库中提供的API即可使用。
库主要由负责信息检索的 [`Roster`](https://github.com/BYOUINZAKA/DD-Emblem/blob/2e289bfb405748a60e0025704639122812b48c68/DDEmblem/Base.py#L6) 和负责领取奖品的 [`Receiver`](https://github.com/BYOUINZAKA/DD-Emblem/blob/2e289bfb405748a60e0025704639122812b48c68/DDEmblem/Engine.py#L12) 组成，详细使用方法请参阅 [Demo.py](https://gitee.com/AnnMaomao/DD-Emblem/blob/master/Demo.py)  中的注释。

以下是运行预览

![运行预览](pic\result.png)

## 注意事项

虽然本工具的效率较为可观，但经测试表明，在直播高峰期如果频繁的领取大量奖品有小概率导致IP在 https://link.bilibili.com 开头的域名上短暂被ban，被ban时间大约为一小时，如要避免需要手动降速。

可以在 `Receiver.Start()` 的参数中引入 `merge` 来提高串行运行的程度以及藉由 `delay` 制造延迟降低领取频率，如 `Receiver(headers).Start(roster, merge=10, delay=0.1)`，或是引入 `proxy` 参数来使用代理。

[Demo.py](https://gitee.com/AnnMaomao/DD-Emblem/blob/master/Demo.py) 中演示了如何按照不同时段选择合适的参数来防止被ban。
但还是要注意如果领取的过程被中断，请等待一段时间再重新领取，以及请勿同时启动多个领取程序。

## 作者信息
GitHub：https://github.com/BYOUINZAKA

知乎： https://www.zhihu.com/people/byouinzaka
## 版权信息

该项目签署了 MIT 授权许可，详情请参阅 [LICENSE](https://github.com/BYOUINZAKA/DD-Emblem/blob/master/LICENSE)
