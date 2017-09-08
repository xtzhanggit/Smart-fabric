import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象，用IPv4通信，协议为TCP(family, type)
host = socket.gethostname()  # 得到当前主机名
ip_port = ('', 1375)  # server的ip一般为空
s.bind(ip_port)
s.listen(5)  # 最多连接数
c, addr = s.accept()  # c为新的socket对象，addr为客户的internet地址
print('Got a new connection from', addr)
data0=0
data1=0
data2=0
while True:
    data = c.recv(1024).decode()
    data=json.loads(data)
    if (data0!=data[0]) | (data1!=data[1]) & (data2!=data[2]): 
        print("a账户余额:%d" % data[0])
        print("b账户余额:%d" % data[1])
        print("c账户余额:%d" % data[2])
        print('\n'+'\n')
    data0=data[0]
    data1=data[1]
    data2=data[2]
