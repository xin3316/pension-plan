# 退休金计划 - 个人开源自动化交易项目

#### 免责条款
- 本项目源码不得用于商业用途需得到项目商用许可，当前仅可用于技术验证和兴趣研究，任何商业用途责任均与项目发起人无关。

 **多平台同步开发中，欢迎大家参与共创开发** 
- Gitee主库：https://gitee.com/xin3316/pension-plan
- Github镜像地址：https://github.com/xin3316/pension-plan
- QQ群：41372623 

#### 项目计划介绍
本计划是通过开发一套自动化交易软件，通过能各种选股策略进行测试和回测，并按计划进行模拟交易，理想的策略成功率达到70%以上和周收益率均达到5%及以上。
#### 本计划特点
1. 个性化交易策略：自动根据网络新闻梳理热点
2. 自动化交易：模拟交易测试收益率
3. 选股策略：多种软件优选策略，重点突出人性化选股，以及AI智能选股，支持多种策略接入的能力。因为A股风格变化太快，希望通过更加灵活的选股策略来抵消风险，提高收益率。
4. 选股范围：AI人工智能选股
5. 开源分支计划：计划以A股、港股ETF(T+0)、美股ETF(T+0)、A股正股/可转债（T+0）共振。
#### 软件环境
- [ _pycharm2024.1.4_ ](https://download.jetbrains.com.cn/python/pycharm-professional-2024.1.4.exe) 官网下载地址：[https://download.jetbrains.com.cn/python/pycharm-professional-2024.1.4.exe](https://download.jetbrains.com.cn/python/pycharm-professional-2024.1.4.exe)
- [ _Python3.8-32位_ ](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe) 官网下载地址：[https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe)

#### 软件架构
软件架构说明
- [数据接口Ashare](https://github.com/mpquant/Ashare) 
- [数据策略分析pytdx](https://gitee.com/better319/pytdx) 


#### 安装教程

1. 下载源码，使用 _PyCharm_ 打开项目；
2. 运行输入： _%APPDATA%_ 
，创建 _pip_ 目录，新建 _pip.ini_ 文件，内容如下
```
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host= mirrors.aliyun.com
```

3.  更新pip

```
pip install --upgrade pip
```

4.  安装模块

```
pip install easyquotation easyutils tushare pandas pywinauto
```


#### 使用说明

1.  策略测试
2.  个人交易服务开启

```
Python.exe run.py
```
3.  个人交易策略监测和自动下单

```
Python.exe trade/AutoTrade.py
```

#### 参与贡献


- 欢迎全球热爱开发和股票量化交易，并热爱开源共创的有志之士共同参与项目开发，共同成就养老金计划！
- QQ群：41372623

![输入图片说明](微信群.jpg)
