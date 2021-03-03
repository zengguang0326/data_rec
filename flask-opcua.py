#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:zengguang
@file: flask-mqtt.py
@time: 2020/12/3 16:22
"""
#encoding: utf-8
from flask import Flask, request, jsonify
from opcua_client import main_c

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/opcua',methods=['GET'])
def opcua_client():
    # global msg, rs
    msg=None
    rs=None
    try:
        url=request.args.get("url")
        url_p="opc.tcp://"+url
        msg,rs=main_c(url_p)
    except Exception as e:
        print(e)
        return jsonify(rescode=500, resmsg=msg,data=rs)
    return jsonify(rescode=200, resmsg=msg,data=rs)

# 发布成opcua server
@app.route('',methods=[''])
def opcua():
    pass




if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5555,debug=True)
