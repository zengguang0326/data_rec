#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:zengguang
@file: client2.py
@time: 2021/2/1 14:05
"""
from opcua import Client, ua
url = "opc.tcp://127.0.0.1:12345/"
# url = "opc.tcp://127.0.0.1:12346/test"
c = Client(url)
try:
    c.connect()
    # root = c.find_servers()
    root = c.get_node('ns=2;i=11').get_value()
    print(root)
    # print("\r\nBrower:")
    # brower_child2(root.get_child(["0:Objects"]), -1, ["Server"])
except Exception as e:
    print("Client Exception:", e)
finally:
    c.disconnect()