# encoding: utf-8

import socket
import json

## a向b(卖家)发起询问
def a_order_ask(weight,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
    ip_port = ('192.168.1.10', port)  # 局域网server的ip，公共端口号
    s.connect(ip_port)
    weight=str(weight) ## 转为str型，才可发送
    s.send(weight.encode())
    data = s.recv(1024).decode()  # 解析二进制流，转字符串
    data=json.loads(data)
    s.close()
    intx=data[0] ## 1为货源充足,0为货源不足
    stringx=data[1]  ## 卖家反馈信息
    return intx,stringx

