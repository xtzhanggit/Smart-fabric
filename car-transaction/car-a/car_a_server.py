# encoding: utf-8

import socket
import time

## 等待b发车通知,用2017端口,收到socket连接后即刻退出通信
def a_receive_wait():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象，用IPv4通信，协议为TCP(family, type)
    ip_port = ('', 2017)  # server的ip一般为空
    s.bind(ip_port)
    s.listen(5)  # 最多连接数
    c, addr = s.accept()  # c为新的socket对象，addr为客户的internet地址
##    print('Got a new connection from', addr)
    data = c.recv(1024).decode()
    c.close()
    print("\033[1;31;47mReceive the information of goods from seller b\033[0m")
    


