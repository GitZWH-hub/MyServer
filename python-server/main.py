#!/usr/bin/env python
# -*-coding:utf-8 -*-
import json
import time

import matplotlib.pyplot as plt
from DataSrc import Futures, TradeCal, HisQuotes, FutSettle
from flask import Flask, Response, request
from BackTest.BackTest import BackTester
from BackTest.DoubleMovingAverage import DoubleMovingAverage
from BackTest.ARIMA import ARIMAStrategy
from FutMapExchange import FutMapExchange
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 线程池
threadPool = ThreadPoolExecutor(max_workers=3)


@app.route("/health")
def health():
    result = {'status': 'UP'}
    return Response(json.dumps(result), mimetype='application/json')


def formatDate(date):
    return date.replace('-', '')


# 8001: 获取交易所下所有期货代码
def getFuture(data):
    result = []
    for key in FutMapExchange:
        if FutMapExchange.get(key)[0] == data['exchange']:
            result.append([key, FutMapExchange.get(key)[1]])

    return Response(json.dumps(result), mimetype='application/json')


# 8002: pull data from tushare  # (<type>/<exchange>/<start>/<end>)
def pullData(data):
    type = data['type']
    res = {'status': 'sucess', 'type': type}
    rsp = Response(json.dumps(res), mimetype='application/json')
    exchange = data['exchange']

    # 期货合约信息
    if type == '1':
        with Futures(exchange) as fut:
            print("en")
            fut.pull()
        return rsp

    start = formatDate(data['start'])
    end = formatDate(data['end'])
    # 交易日历
    if type == '2':
        with TradeCal(exchange) as tc:
            tc.pull(start_date=start, end_date=end)
    # 历史行情
    elif type == '3':
        with HisQuotes(exchange) as hq:
            hq.pull(start_date=start, end_date=end)
    # 结算参数
    elif type == '4':
        with FutSettle(exchange) as fs:
            fs.pull(start_date=start, end_date=end)

    return rsp


# 8008 回测：下载数据      /<fut>/<start>/<end>
def getKData(data):
    start = formatDate(data['start'])
    end = formatDate(data['end'])
    fut = data['fut']
    short = int(data['shortT'])
    long = int(data['longT'])
    # 自动获取fut所在的交易所
    if fut[:2].upper() not in FutMapExchange:
        res = {"fail": "合约不存在，请重新填写"}
        return Response(json.dumps(res), mimetype='application/json')
    exchange = FutMapExchange.get(fut[:2].upper())[0]

    with HisQuotes(exchange) as hq:
        data = hq.getData(ts_code=fut, start=start, end=end, short=short, long=long)
    print(data)
    return Response(json.dumps(data.to_json(orient='records')), mimetype='application/json')


# 8003
def getStockInfo(data):
    import pandas as pd
    # 1. 读取‘HS300_name.csv文件’,获取到300只股票的'Constitudent Code','Constitudent Name','Exchange','weight'.
    path = '/Users/zhangwh/Desktop/量化/MyServer/python-server/HS300_name.csv'
    df = pd.read_csv(path, dtype=str)
    stock_info = df.loc[:, [x for x in df.columns.tolist() if x in ['Date', 'IndexName', 'Code', 'Name', 'Name(Eng)', 'Exchange', 'weight']]]

    return Response(json.dumps(stock_info.to_json(orient='records')), mimetype='application/json')


# 短连接请求
@app.route("/short", methods=["GET", "POST"])
def shortRequestDistribute():
    data = request.get_data()
    data = json.loads(data)
    print("收到数据", data)
    # 交易代码
    code = data['code']
    functions = {
        "8001": getFuture,
        "8002": pullData,
        "8008": getKData,
        "8003": getStockInfo
    }
    return functions.get(code)(data)


'''---------------------------------    分    界    线    ----------------------------------'''

# from real_so.md_demo import Controller
#
# controller = Controller()
#

# # 修改8101支持新增订阅合约：
# # 逻辑：python服务启动即链接行情服务，但此时无合约订阅，通过本接口实现添加合约并订阅。理论上是可行的，后续可开发取消某个合约的订阅
# @app.route("/8101/<fut>/<futEnd>", methods=["GET", "POST"])
# def getQuotes(fut, futEnd):
#     # controller.start()
#     print("8101订阅")
#     futEnd = formatDate(futEnd)
#     fut_code = fut + futEnd[2:]
#     controller.addFutCode(fut_code=fut_code.lower())
#     controller.stop()
#     controller.start()
#
#     return "success"
#
#
# # 8102  取消订阅行情
# @app.route("/8102", methods=["GET"])
# def stopQuotes():
#     print('取消订阅行情')
#     controller.stop()
#     return "success"
#
#
# # 8103  更改行情环境
# @app.route("/8103/<flag>", methods=["GET", "POST"])
# def exchangeEV(flag):
#     print('更改行情环境')
#     controller.setEV(flag=flag)
#     return "success"


# 8105  双均线回测 ['start', 'end', 'long', 'short', 'cash', 'fut']
def doubleMABackTest(data):
    print("开始双均线回测")
    start = data['start'].replace('-', '')
    end = data['end'].replace('-', '')
    """
    设置策略实例参数
    """
    # 双均线策略
    doubleMABT = DoubleMovingAverage()
    # 设置长线周期
    doubleMABT.set_long(data['long'])
    # 设置短线周期
    doubleMABT.set_short(data['short'])
    """
    设置回测模块相关的参数
    """
    # 回测
    backTester = BackTester()
    # 设置策略类
    backTester.set_strategy_instance(doubleMABT)
    # 设置初始资金
    backTester.set_cash(data['cash'])
    # 设置期货代码
    backTester.set_tsCode(data['fut'])
    # 设置起始结束日期
    backTester.set_date(start, end)
    # 启动回测
    backTester.start()


# 8106  ARIMA策略回测
def ARIMAtest(data):  # dataset
    print("开始ARIMA策略回测")
    start = data['start'].replace('-', '')
    end = data['end'].replace('-', '')
    """
    设置策略实例参数
    """
    ARIMA_instance = ARIMAStrategy()
    ARIMA_instance.set_train_nums(int(data['nums']))
    """
    设置回测模块相关的参数
    """
    # 回测
    backTester = BackTester()
    # 设置策略类
    backTester.set_strategy_instance(ARIMA_instance)
    # 设置初始资金
    backTester.set_cash(data['cash'])
    # 设置期货代码
    backTester.set_tsCode(data['fut'])
    # 设置起始结束日期
    backTester.set_date(start, end)
    # 启动回测
    backTester.start()

    return 'success'


# 9000 下载股票行情数据，并生成相关的html文件    [start,end,ts_code]
def createStockHTML(data):
    from Data.GetData import create_html
    create_html(data['ts_code'], data['start'], data['end'])


# 长连接请求根据code代码分发业务接口
@app.route("/request", methods=["GET", "POST"])
def longRequestDistribute():
    data_set = request.get_data()
    print(data_set)
    data_set = json.loads(data_set)
    print("收到数据", data_set)
    # 交易代码
    code = data_set['code']

    functions = {
        "8106": ARIMAtest,
        "8105": doubleMABackTest,
        "9000": createStockHTML,
    }
    # 线程池，异步
    task = threadPool.submit(functions.get(code), data_set)
    print(task.done())

    return {"result": "success"}


if __name__ == "__main__":
    app.run(port=3001, host='0.0.0.0')
