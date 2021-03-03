#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:zengguang
@file: ttt.py
@time: 2020/9/2 18:52
"""
aaa={'namea': 'node1', 'statusa': 'good'}
bbb={'namea': 'node3', 'statusb': 'good'}
# aa={'node1': Node(NumericNodeId(ns=2;i=2)),'node2': Node(NumericNodeId(ns=2;i=3)), 'node3': Node(NumericNodeId(ns=2;i=4)), 'node4': Node(NumericNodeId(ns=2;i=5)), 'node5': Node(NumericNodeId(ns=2;i=6)), 'node6': Node(NumericNodeId(ns=2;i=7)), 'node7': Node(NumericNodeId(ns=2;i=8)), 'node8': Node(NumericNodeId(ns=2;i=9)), 'node9': Node(NumericNodeId(ns=2;i=10)), 'node10': Node(NumericNodeId(ns=2;i=11))}
print(type(aaa.keys()))
print(type(bbb.keys()))
print(type(aaa.keys() & bbb.keys()))