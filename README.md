# wechat-agent

wechat-agent是一个Windows平台下能够自动化回复微信消息的代理应用程序。可以使用它来自动回复一些规则下的微信消息。wechat-agent提供两种代理模式。
1. 指定回复（简单）模式
2. AI回复（AI问答）模式

-----

## 说明

- [安装](#安装)
- [运行](#运行)

## 安装和运行

### 默认

```shell
pip install wechat-agent

#将使用默认端口8080
wechat-agent
```
浏览器访问 http://127.0.0.1:8080/ui/index.html

### 指定IP端口

```shell
#将使用8000端口，并使用绑定ip到192.168.31.66
wa_port=8000 wa_host=192.168.31.66 wechat-agent
```
浏览器访问 http://192.168.31.66:8000/ui/index.html

值得一提的是，wechat-agent默认绑定的IP是0.0.0.0全网段，如果设置`wa_host`为具体的某个局域网IP或者**127.0.0.1** 请使用具体IP访问或者127.0.01访问。

## 开发接入

```shell
git clone https://gitee.com/zjwan461/wechat-agent.git
cd wechat-agent
pip install -e .
cd ui
npm install

# 前端
cd ui
npm run dev
# 后端
python main.py
```

