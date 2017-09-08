from car_b_fabric import *
import time
import socket
import ctypes
# encoding: utf-8

import threading
from switch import Switch

flag=2 ## 用来判断小车是否到达,1到,0未到

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


## 等待函数,上限
def loop():
    timekeeping = 0
    print("\033[1;31;47mStart the timekeeping for 60 secends\033[0m")
    
    while timekeeping <= 30:
        timekeeping += 1
        print(timekeeping)
        time.sleep(1)
    global flag
    flag=0  ## 30秒后,车未到,flag置为0


## 接受rfid信息
def b_receive_car():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象，用IPv4通信，协议为TCP(family, type)
    ip_port = ('', 4444)  # server的ip一般为空
    s.bind(ip_port)
    s.listen(5)  # 最多连接数3
    c, addr = s.accept()  # c为新的socket对象，addr为客户的internet地址
##    print('Got a new connection from', addr)
    data = c.recv(1024).decode()
    c.close()
    global flag
    flag = 1   ## 车到之后,flag置为1
    terminate_thread(tloop)  ## 车到后即刻杀死计时进程


## b接受订单
def b_receive_order(weight,percentage,b_value1):
    advance_payment=int(weight*10*percentage) ## 预付金额
    while True:
        time.sleep(5)  ## 等待5秒,保证交易被确认
        b_value2 = get_value('b') ## 再次查询金额
        if b_value2==(b_value1+advance_payment): ## 预付成功
            print("\033[1;31;47mReceipt the advance_payment from buyer a:%d,the value of b is:%d\033[0m"%(advance_payment, b_value2))
            
            insurance=10 ## 保险费
            invoke('b','c',insurance)  ## 买保险
            b_value3 = get_value('b') ## 再次查询金额
            print("\033[1;31;47mPurchase the insurance of goods:%d,the value of b is:%d\033[0m" %(insurance ,b_value3))
            
            break
    return b_value3 ## 返回收到预付金的b账户余额


## 启动小车进程
def start_car():
    ## 启动小车
    a = Switch('switch002','host_remote')
    a.execute('on') ## 启动小车
    print("\033[1;31;47mStart the car\033[0m")
    time.sleep(3)
    a.execute('off') ## 关闭小车


## b等待收货通知
def b_wait_information(weight,percentage,b_value2):
    advance_payment=int(weight*10*percentage) ## 预付款
    balance_payment=int(weight*10*(1-percentage)) ## 尾款
    global tloop  ## 设置计时进程为全局变量,否则无法在接受rfid进程中杀死计时进程
    tloop = threading.Thread(target=loop) ## 等待计时进程
    tsocket = threading.Thread(target=b_receive_car) ## 接受rfid进程
    tloop.start()  ## 计时进程开始
    tsocket.start()  ## 接受rfid进程开始
    tloop.join()  ## 等待计时进程结束
    terminate_thread(tsocket)  ## 杀死接受rfid进程
    if flag==1: ## 小车到
        time.sleep(5) ## 等待10s,保证尾款交易确认
        b_value3=get_value('b')
        if b_value3==(b_value2+balance_payment):
            print("\033[1;31;47mReceipt the balance_payment from a:%d,the value of b is:%d\033[0m"%(balance_payment ,b_value3))
            
            
    else: ## 超时未收货
        print("\033[1;31;47mThe car did't arrive.Transfer the advance_payment to buyer a\033[0m")
        invoke('b','a',advance_payment)  ## b给a返钱
        rebate=100 ## 返利
        invoke('c','b',rebate) ## c给b返保
        print("\033[1;31;47mThe buyer a didn't receipt the goods.Receipt the refund from insurance company:%d,the value of b is:%d\033[0m"%(rebate ,get_value('b')))
        


            
