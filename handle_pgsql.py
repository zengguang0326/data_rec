#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:zengguang
@file: handle_pgsql.py
@time: 2020/9/18 14:50
"""

import psycopg2
# from . import POSTGRESQL_DATABASE,POSTGRESQL_USER,POSTGRESQL_PASSWORD,POSTGRESQL_PORT,POSTGRESQL_HOST
#POSTGRESQL_HOST = '127.0.0.1'
POSTGRESQL_HOST = '192.168.61.186'
POSTGRESQL_PORT = '5432'
POSTGRESQL_DATABASE = "opc"
POSTGRESQL_USER = "postgres"
POSTGRESQL_PASSWORD = "postgres"
class HandlePostgresql:
    def __init__(self):
        self.conn = psycopg2.connect(database=POSTGRESQL_DATABASE, user=POSTGRESQL_USER, password=POSTGRESQL_PASSWORD,
                                     host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
        self.curs = self.conn.cursor()
    # pass
    # def conn_postgresql(self):
    #     """连接数据库"""
    #     #print(POSTGRESQL_HOST,POSTGRESQL_PORT,POSTGRESQL_DATABASE,POSTGRESQL_PASSWORD,POSTGRESQL_USER)
    #     self.conn = psycopg2.connect(database=POSTGRESQL_DATABASE, user=POSTGRESQL_USER, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
    #     self.cur = self.conn.cursor()
    #
    #
    def execute_sql(self, sql):
        """执行操作数据的相关sql"""
        self.curs.execute(sql)

    def search(self, sql):
        """执行查询sql"""
        self.curs.execute(sql)
        return self.curs.fetchall()

    def commit_po(self):
        self.conn.commit()

    def rollback_po(self):
        self.conn.rollback()

    def close_postgresql(self):
        """关闭数据库连接"""
        self.curs.close()
        self.conn.close()



if __name__ == '__main__':
    test = HandlePostgresql()
    sql = "select * from test"
    for i in test.search(sql):
        print(i)