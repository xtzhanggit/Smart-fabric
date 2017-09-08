# encoding: utf-8

import socket
import json
import time

## 检验订单是否符合条件,返回最后符合要求的订单份数
def b_receive_wait():
    port=1025 ## 初始端口为1025
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象，用IPv4通信，协议为TCP(family, type)
        ip_port = ('', port)  # server的ip一般为空
        s.bind(ip_port)
        port+=1  ## 端口号加1,避免下次端口堵塞
        s.listen(5)  # 最多连接数
        c, addr = s.accept()  # c为新的socket对象，addr为客户的internet地址
##        print('Got a new connection from', addr)

        a = [0] * 2
        data = c.recv(1024).decode()
        if data:  ##　client发来消息
            print('from buyer a:' + data)
            if int(data) > 45:
                flag= 0
                flag= str(flag)
                a[0]=0  ## 0为货源不足,1为货源充足
                a[1]="Sorry!We don't have enough goods,and send back the money to your account." ## 卖家反馈信息
                json_str = json.dumps(a) ## 打包成json数据类型,方便发送
                c.send(json_str.encode())
            else:
                flag = 1
                flag = str(flag)
                a[0]=1  ## 0为货源不足,1为货源充足
                a[1]="We have accepted your order."  ## 卖家反馈信息
                json_str = json.dumps(a) ## 打包成json数据类型,方便发送
                c.send(json_str.encode())
                break
        else: ## client无消息时，继续等待
            time.sleep(3)
        c.close()

    return int(data) ## 返回最后订购件数

