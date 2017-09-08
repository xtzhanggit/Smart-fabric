# encoding: utf-8

from car_a_fabric import *
import socket
import time
import ctypes
import threading

flag=2 ## 用来判断小车是否到达,1到,0未到,初始值用2

## 杀死进程函数
def terminate_thread(thread):
    if not thread.isAlive():
        return
    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


## 计时进程,上限30秒
def loop():
    timekeeping = 0
    print("\033[1;31;47mStart the timekeeping for 60 secends\033[0m")
    
    while timekeeping <= 30:
        timekeeping += 1
        print(timekeeping)
        time.sleep(1)
    global flag   ## 30秒后,车未到,flag置为0
    flag=0


## 接受rfid信息进程
def a_wait_car():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象，用IPv4通信，协议为TCP(family, type)
    ip_port = ('', 3333)  # server的ip一般为空
    s.bind(ip_port)
    s.listen(5)  # 最多连接数3
    c, addr = s.accept()  # c为新的socket对象，addr为客户的internet地址
##    print('Got a new connection from', addr)
    data = c.recv(1024).decode()
    c.close()
    global flag ## 车到之后,flag置为1
    flag = 1
    terminate_thread(tloop) ## 车到后即刻杀死计时进程


## a发起订单,向卖家转预付金,买东西
def a_order(weight,percentage):
    advance_payment=weight*10*percentage ## 预付金额
    invoke('a','b',advance_payment) ## 向卖家付定金
    print("\033[1;31;47mTransfer the advance_payment to seller b:%d,the value of a is:%d\033[0m"%(advance_payment, get_value('a'))) ## 得到a的账户余额
    


## a等待小车到达,收货
def a_take_delivery(weight,percentage):
    value1 = get_value('a')
    balance_payment=weight*10*(1-percentage) ## 尾款
    advance_payment=weight*10*percentage ## 预付款
    global tloop ## 设置计时进程为全局变量,否则无法在接受rfid进程中杀死计时进程
    tloop = threading.Thread(target=loop) ## 计时进程
    tsocket = threading.Thread(target=a_wait_car) ## 接受rfid进程
    tloop.start() ## 计时进程开始
    tsocket.start() ## 接受rfid进程开始
    tloop.join() ## 等待计时进程结束
    terminate_thread(tsocket) ## 杀死接受rfid进程
    if flag==1: ## 小车到
        invoke('a','b',balance_payment) ## a给b打尾款
        print("\033[1;31;47mThe car has arrived.Transfer the balance_payment to seller b:%d,the value of a is:%d\033[0m"%(balance_payment, get_value('a')))
        
##        print("a has received the goods")
    else: ## 超时未收货
        print("\033[1;31;47mThe car did't arrive.Waiting the refund from seller b\033[0m")
        
        while True:
            if get_value('a') == (value1+advance_payment):
                print("\033[1;31;47mReceipt the refund:%d,the value of a is:%d\033[0m"%(advance_payment ,get_value('a')))
                
                break

