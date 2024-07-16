# -*- coding: utf-8 -*-  

from flask import Flask, request, jsonify
import functools
import time
import ast
import threading
import requests
import json
from loguru import logger
import easytrader
from easytrader import refresh_strategies 
from easytrader import grid_strategies  
      
   
logger.add('./logs/api_{time}.log', rotation='00:00', encoding='utf-8') 

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#交流讨论+威信: gupiao888nb 
client_path = 'C:/同花顺软件/同花顺/xiadan.exe'
ip = ""
token = 'token'
dd_token = 'key'
 
  

logger.info(client_path  + " 准备连接")
user = easytrader.use('universal_client')
user.connect(client_path)  # 类似 r'C:\htzqzyb2\xiadan.exe'
logger.info(client_path  + " 连接成功")
user.refresh_strategy = refresh_strategies.Toolbar(refresh_btn_index=4)
user.grid_strategy = grid_strategies.WMCopy
#user.grid_strategy_instance.tmp_folder = 'D:\\12345'
user.enable_type_keys_for_editor() #如遇到无法输入验证码，请注释此行。



def dingding(text):
    try:
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % dd_token
        json_text = to_msg(text)
        resp = requests.post(api_url,
                             json.dumps(json_text),
                             headers=headers,
                             timeout=15).text
    except Exception as e:
        print(e)
 

def to_msg(text):
    json_text = {
        "msgtype": "text",
        "at": {
            "atMobiles": [],
            "isAtAll": False
        },
        "text": {
            "content": ip + text
        }
    }
    return json_text


lock = threading.Lock()
next_time = 0
interval = 5  #5秒一次

def interval_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global interval
        global lock
        global next_time
        lock.acquire()
        now = time.time()
        if now < next_time:
            time.sleep(next_time - now)
        try:
            rt = func(*args, **kwargs)
        except Exception as e:
            rt = ({'code': 1, 'status': 'failed', 'msg': '{}'.format(e)}, 400)
        next_time = time.time() + interval
        lock.release()
        return rt

    return wrapper


def parse_webhook(webhook_data):
    data = ast.literal_eval(webhook_data)
    return data


# Create root to easily let us know its on/working.
@app.route('/')
def root():
    return 'trade api'

#账户资金信息
@app.route('/api/balance', methods=['GET'])
@interval_call
def get_balance():
    req_token = request.args['token']
    if token == req_token:
        data = user.balance
        result = {'code': 0, 'status': 'success', 'msg': 'ok', 'data': data} 
    else:
        result = {'code': 1, 'status': 'failed', 'msg': 'token is error'}
    return jsonify(result), 200


#账户持仓信息
@app.route('/api/position', methods=['GET'])
@interval_call
def get_position():
    req_token = request.args['token']
    if token == req_token:
        data = user.position
        result = {'code': 0, 'status': 'success', 'msg': 'ok', 'data': data} 
    else:
        result = {'code': 1, 'status': 'failed', 'msg': 'token is error'}
    return jsonify(result), 200


#查询当日成交
@app.route('/api/orders/today', methods=['GET'])
@interval_call
def get_today_ok_orders():
    req_token = request.args['token']
    if token == req_token:
        data = user.today_trades
        result = {'code': 0, 'status': 'success', 'msg': 'ok', 'data': data} 
    else:
        result = {'code': 1, 'status': 'failed', 'msg': 'token is error'}
    return jsonify(result), 200


#查询当日委托 (包括已成交/未成交/已撤单)
@app.route('/api/orders/filled', methods=['GET'])
@interval_call
def get_filled_orders():
    req_token = request.args['token']
    if token == req_token:
        data = user.today_entrusts
        result = {'code': 0, 'status': 'success', 'msg': 'ok', 'data': data} 
    else:
        result = {'code': 1, 'status': 'failed', 'msg': 'token is error'}
    return jsonify(result), 200


#卖出
@app.route('/api/sell', methods=['POST'])
@interval_call
def sell():
    data = parse_webhook(request.get_data(as_text=True))
    # Check that the key is correct
    result = {}
    if token == data['token']:
        stock = data['code']
        amount = data['amount']
        price = data['price']
        is_market = data['is_market']
        data = None
        if is_market:
            data = user.market_sell(stock,amount=int(amount))
        else:
            data = user.sell(stock, price=price, amount=int(amount))
        result = {'code': 0, 'status': 'success', 'msg': 'ok', 'data': data}     
    else:
        result = {'code': 1, 'status': 'failed', 'msg': 'token is error'}
    return jsonify(result), 200


#买入
@app.route('/api/buy', methods=['POST'])
@interval_call
def buy():
    data = parse_webhook(request.get_data(as_text=True))
    # Check that the key is correct
    result = {}
    if token == data['token']:
        stock = data['code']
        amount = data['amount']
        price = data['price']
        is_market = data['is_market']
        data = None
        if is_market:
            data = user.market_buy(stock,amount=int(amount))
        else:
            data = user.buy(stock, price=price, amount=int(amount))
        result = {'code': 0, 'status': 'success', 'msg': 'ok', 'data': data}    
    else:
        result = {'code': 1, 'status': 'failed', 'msg': 'token is error'}
    return jsonify(result), 200



#撤单 需要从买入卖出时 获取 订单号 保存
@app.route('/api/cancel', methods=['GET'])
@interval_call
def cancel():
    entrust_no = request.args['entrust_no']
    req_token = request.args['token']
    if token == req_token:
        logger.info(entrust_no)
        data = user.cancel_entrust(entrust_no)
        result = {'code': 0, 'status': 'success', 'msg': 'ok', 'data': data}
    else:
        result = {'code': 1, 'status': 'failed', 'msg': 'token is error'}
    return jsonify(result), 200


if __name__ == '__main__':
    # gevent 
    from gevent import monkey 
    from gevent.pywsgi import WSGIServer 
    monkey.patch_all() 
    # gevent end 
    http_server = WSGIServer(('0.0.0.0', int(801)), app) 
    http_server.serve_forever()
