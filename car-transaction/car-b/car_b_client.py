# encoding: utf-8

import socket
import time

## b通知a小车出发
def b_inform_a():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
    ip_port = ('192.168.1.10', 2017)  # 局域网server的ip，公共端口号
    s.connect(ip_port)
    s.send("The car of goods is on the way".encode())
    print("\033[1;31;47mInform buyer a that the goods are on the way\033[0m")
    
    s.close

