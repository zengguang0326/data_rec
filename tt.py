# import time
# import os
#
# # 获取进程的pid
# pid = os.getpid()
# print('pid: ', pid)
#
# # 将pid写入本地文件
# f1 = open(file='count_pid.txt', mode='w')
# f1.write(pid.__str__())
# f1.close()
#
# # 开始计数并打印
# n = 0
# while True:
#     n += 1
#     print(n)
#     time.sleep(1)

#!usr/bin/env python
#-*- coding:utf-8 _*-
# author=baird_xiang
import os
import time
import re
import copy

nginxRestart_num = -1
nginxReload_num = -1
logSender_num = -1
es_num = -1
nginxParent_pid = []
nginxChild_pid = []
logSender_pid = []
es_pid = []

nginxRestart_time = []
nginxReload_time = []
logSender_time = []
es_time = []


def get_restart(thread_name):
    global nginxRestart_num, nginxReload_num, logSender_num, es_num
    while True:
        try:
            for i in thread_name:
                if i == 'nginx_restart':
                    nP_pid = os.popen("sudo pgrep -lo nginx |grep -v grep|awk '{print $1}'").read()
                    nP_time = os.popen("sudo ps aux|grep nginx |grep -v grep|awk 'NR==1{print $9}'").read()
                    nginx_path = os.popen("sudo ps aux|grep nginx |grep -v grep|awk 'NR==1{print $11}'").read()
                    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    nP_time_now = date + '-' + nP_time.split('\n')[0]
                    if nP_pid and (nP_pid not in nginxParent_pid) and (nginx_path == '/usr/sbin/nginx\n'):
                        nginxParent_pid.append(nP_pid)
                        nginxRestart_num = nginxRestart_num + 1
                        # if nP_time and (nP_time_now not in nginxRestart_time) and (color!='-c\n'):
                        nginxRestart_time.append(nP_time_now)

                elif i == 'nginx_reload':
                    nR_pid = os.popen("sudo pgrep -ln nginx|grep -v grep |awk '{print $1}'").read()
                    nR_time = os.popen("sudo ps aux|grep nginx |grep -v grep|awk 'NR==2{print $9}'").read()
                    nginx_path = os.popen("sudo ps aux|grep nginx |grep -v grep|awk 'NR==1{print $11}'").read()
                    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    nR_time_now = date + '-' + nR_time.split('\n')[0]
                    if nR_pid and (nR_pid not in nginxChild_pid) and (nginx_path == '/usr/sbin/nginx\n'):
                        nginxChild_pid.append(nR_pid)
                        nginxReload_num = nginxReload_num + 1 - nginxRestart_num
                        # if nR_time and (nR_time_now not in nginxReload_time) and (color!='-c\n'):
                        nginxReload_time.append(nR_time_now)

                elif i == 'log_sender':
                    lS_pid = os.popen("sudo ps aux|grep log_sender |grep -v grep|awk 'NR==1{print $2}'").read()
                    lS_time = os.popen("sudo ps aux|grep log_sender |grep -v grep|awk 'NR==1{print $9}'").read()
                    color = os.popen("sudo ps aux|grep log_sender |grep -v grep|awk 'NR==1{print $12}'").read()
                    wwwdate = os.popen("sudo ps aux|grep log_sender |grep -v grep|awk 'NR==1{print $1}'").read()
                    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    lS_time_now = date + '-' + lS_time.split('\n')[0]
                    if lS_pid and (color != '-c\n') and (lS_pid not in logSender_pid) and (wwwdate == 'www-data\n'):
                        logSender_pid.append(lS_pid)
                        logSender_num = logSender_num + 1
                        # if lS_time and (lS_time_now not in logSender_time) and (color!='-c\n'):
                        logSender_time.append(lS_time_now)
                elif (i == 'elasticsearch') and (
                os.popen("sudo ps -ef |grep elasticsearch |grep -v grep|awk 'NR==1{print $2}'").read()):
                    time.sleep(1)
                    e_pid = os.popen("sudo ps aux|grep elasticsearch |grep -v grep|awk 'NR==1{print $2}'").read()
                    e_time = os.popen("sudo ps aux|grep elasticsearch |grep -v grep|awk 'NR==1{print $9}'").read()
                    color = os.popen("sudo ps aux|grep elasticsearch |grep -v grep|awk 'NR==1{print $12}'").read()
                    elastic = os.popen("sudo ps aux|grep elasticsearch |grep -v grep|awk 'NR==1{print $1}'").read()
                    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    e_time_now = date + '-' + e_time.split('\n')[0]
                    if e_pid and (color != '-c\n') and (e_pid not in es_pid) and (elastic == 'elastic+\n'):
                        es_pid.append(e_pid)
                        es_num = es_num + 1
                        # if e_time and (e_time_now not in es_time) and (color!='-c\n') and (elastic =='elastic+\n'):
                        es_time.append(e_time_now)
                else:
                    pass
        except (OSError, IOError):  # 防止进入循环但是这个时候进程重启，导致popen读取不到进程信息就会出错
            pass


def set_nginxRestart_txt():
    now_path = os.getcwd()
    file_name = now_path + '/nginxRestart_%s.txt' % (nginxRestart_time[-1])
    # 写入文本
    file1 = open(file_name, 'w')
    for i in range(1, len(nginxRestart_time)):
        file1.write(
            '重启时间：' + nginxRestart_time[i] + '重启前父进程号: ' + nginxParent_pid[i - 1] + '重启后父进程号: ' + nginxParent_pid[
                i] + '\n')

    file1.close()
    file2 = open(file_name, 'a+')
    file2.write('nginx restart次数为： ' + str(nginxRestart_num) + '\n')
    file2.close()


def set_nginxReload_txt():
    now_path = os.getcwd()
    file_name = now_path + '/nginxReload_%s.txt' % (nginxReload_time[-1])
    # 写入文本
    file1 = open(file_name, 'w')
    for i in range(1, len(nginxReload_time)):
        file1.write('重启时间：' + nginxReload_time[i] + '\n')

    file1.close()
    file2 = open(file_name, 'a+')
    file2.write('nginx reload次数为：' + str(nginxReload_num) + '\n')
    file2.close()


def set_logsender_txt():
    now_path = os.getcwd()
    file_name = now_path + '/logsender_restart_%s.txt' % (logSender_time[-1])
    # 写入文本
    file1 = open(file_name, 'w')
    for i in range(1, len(logSender_time)):
        file1.write(
            '重启时间：' + logSender_time[i] + '重启前进程号: ' + logSender_pid[i - 1] + '重启后进程号: ' + logSender_pid[i] + '\n')

    file1.close()
    file2 = open(file_name, 'a+')
    file2.write('logsender重启次数为: ' + str(logSender_num) + '\n')
    file2.close()


def set_es_txt():
    now_path = os.getcwd()
    file_name = now_path + '/esRestart_%s.txt' % (es_time[-1])
    # 写入文本
    file1 = open(file_name, 'w')
    for i in range(1, len(es_time)):
        file1.write('重启时间：' + es_time[i] + '重启前进程号: ' + es_pid[i - 1] + '重启后进程号: ' + es_pid[i] + '\n')

    file1.close()
    file2 = open(file_name, 'a+')
    file2.write('elasticsearch重启次数为： ' + str(es_num) + '\n')
    file2.close()


if __name__ == "__main__":
    thread_name = ['nginx_restart', 'nginx_reload', 'log_sender', 'elasticsearch']
    try:
        get_restart(thread_name)
    except (KeyboardInterrupt, SystemExit):
        set_nginxRestart_txt()
        set_nginxReload_txt()
        set_logsender_txt()
        set_es_txt()