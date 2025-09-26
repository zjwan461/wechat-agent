# wechat-agent

wechat-agent是一个Windows平台下能够自动化回复微信消息的代理应用程序。可以使用它来自动回复一些规则下的微信消息。wechat-agent提供两种代理模式。
1. 指定回复（简单）模式
2. AI回复（AI问答）模式

-----

## 说明

- [安装](#安装)
- [运行](#运行)

## 安装

### 本地开发依赖安装

```shell
git clone https://gitee.com/zjwan461/wechat-agent.git
cd wechat-agent
pip install -e .
cd ui
npm install
```
浏览器访问 http://127.0.0.1:8001/ui

### 直接安装
```shell
pip install wechat-agent
```
运行
```shell
wechat-agent
```
浏览器访问 http://127.0.0.1:8080/ui/index.html

## 运行

开发接入

```shell
# 前端
cd ui
npm run dev
# 后端
python main.py
```

