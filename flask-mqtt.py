#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:zengguang
@file: flask-mqtt.py
@time: 2020/12/3 16:22
"""
#encoding: utf-8

import eventlet
from flask import Flask, render_template,request,jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_cors import CORS
eventlet.monkey_patch()
from flask_cors import *
app = Flask(__name__)
CORS(app, supports_credentials=True)
from opcua_client import main_c
from handle_pgsql import HandlePostgresql
import json

socketio = SocketIO(app,cors_allowed_origins='*')

@app.route('/')
def index():
    return 'hello'



import re
@app.route('/aa')
def aa():
    global mqtt
    host = request.args.get("host")       # MQTT host
    port = int(request.args.get("port"))  # MQTT port
    topic = request.args.get("topic")     # MQTT topic
    topic2 = request.args.get("topic2")   # socketio topic

    print(app.config.get('MQTT_BROKER_URL'))
    print(app.config.get('MQTT_BROKER_PORT'))

    if app.config.get('MQTT_BROKER_URL')!=host or app.config.get('MQTT_BROKER_PORT')!=port or app.config.get('MQTT_BROKER_TOPIC'):
        app.config['MQTT_BROKER_URL'] = host
        app.config['MQTT_BROKER_PORT'] = port
        app.config['MQTT_BROKER_TOPIC'] = topic
        app.config['MQTT_REFRESH_TIME'] = 1.0
        print(app.config.get('MQTT_BROKER_URL'))
        print(app.config.get('MQTT_BROKER_PORT'))
        print(topic2)
        try:
            mqtt = Mqtt(app)
        except Exception as e:
            rs=''
            print(e)
            if re.findall('\[.*?\] WSAECONNREFUSED', str(e)):
                rs="连接被拒绝"
            elif re.findall('\[.*?\] WSAETIMEDOUT', str(e)):
                rs="连接超时"
            elif re.findall('\[.*?\] No address found', str(e)):
                rs="未找到IP地址"

            return jsonify(rescode=500, resmsg=str(rs))
        # try:
        #
        # except Exception as e:
        #     print(e)
        # print(app.config.get('MQTT_LAST_WILL_TOPIC'))
        # bb(mqtt,topic2)
    # print('MQTT_LAST_WILL_TOPIC===',app.config.get('MQTT_LAST_WILL_TOPIC'))
    # MQTT_LAST_WILL_TOPIC
    mqtt_operat(mqtt,topic2)
    return jsonify(rescode=200, resmsg='success')



def mqtt_operat(mqtt,topic2):
    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        # mqtt.subscribe('/python/mqtt1')
        topic=app.config.get('MQTT_BROKER_TOPIC')
        print(topic)
        mqtt.subscribe(topic)

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        # print(message)
        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )
        # emit a mqtt_message event to the socket containing the message data
        socketio.emit(topic2, data=data)

    @mqtt.on_log()
    def handle_logging(client, userdata, level, buf):
        # print(level, buf)
        pass

    @mqtt.on_disconnect()
    def handle_disconnect():
        print("CLIENT DISCONNECTED")
        mqtt._disconnect()

    @socketio.on('disconnect')
    def aaa():
        print('websocket disconnect')
        mqtt._disconnect()



 
# @app.route('/opcua_client')
# def opcua_client():
#     url = request.args.get("url")
#     rs=main_c(url)
#     return jsonify(rescode=RET.OK, resmsg="OK", data=data_array)

@app.route('/mqttoperate',methods=['POST'])
def insert():
    data = json.loads(request.get_data())
    mqttip = data["mqttip"]
    mqttport = data["mqttport"]
    topic = data["topic"]
    handle_postgresql = HandlePostgresql()
    try:
        sql = "insert into mqtt (mqttip,mqttport,topic) values ('%s','%s','%s')" % (mqttip,mqttport,topic)
        handle_postgresql.execute_sql(sql)
    except Exception as e:
        print(e)
        handle_postgresql.rollback_po()
        return jsonify(rescode=500, resmsg="数据库错误")
    handle_postgresql.commit_po()
    handle_postgresql.close_postgresql()
    return jsonify(rescode=200, resmsg="插入成功")

@app.route('/mqttoperate',methods=['GET'])
def select():
    # request.args.get("host")
    # request.args.get("host")
    # request.args.get("host")
    # topic = data["topic"]
    dataArray = []
    handle_postgresql = HandlePostgresql()
    sql = "select id,mqttip,mqttport,topic from mqtt"
    try:
        rows=handle_postgresql.search(sql)
    except Exception as e:
        print(e)
        handle_postgresql.close_postgresql()
        return jsonify(rescode=500, resmsg="数据库错误")
    for row in rows:
        info={}
        info['id']=row[0]
        info['mqttip']=row[1]
        info['mqttport']=row[2]
        info['topic']=row[3]
        dataArray.append(info)
    handle_postgresql.close_postgresql()
    return jsonify(rescode=200, resmsg="查询成功", data=dataArray)

@app.route('/mqttoperate',methods=['DELETE'])
def delete():
    data = json.loads(request.get_data())
    id = data["id"]
    handle_postgresql = HandlePostgresql()
    try:
        sql = "delete from mqtt where id='%s'" % (id)
        handle_postgresql.execute_sql(sql)
    except Exception as e:
        print(e)
        handle_postgresql.rollback_po()
        handle_postgresql.close_postgresql()
        return jsonify(rescode=500, resmsg="数据库错误")
    handle_postgresql.commit_po()
    handle_postgresql.close_postgresql()
    return jsonify(rescode=200, resmsg="删除成功")

@app.route('/ ',methods=['GET'])
def opcua_client():
    # global msg, rs
    try:
        url=request.args.get("url")
        url_p="opc.tcp://"+url
        msg,rs=main_c(url_p)
    except Exception as e:
        print(e)
        return jsonify(rescode=500, resmsg=msg,data=rs)
    return jsonify(rescode=200, resmsg=msg,data=rs)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=7777 , use_reloader=True, debug=True)


