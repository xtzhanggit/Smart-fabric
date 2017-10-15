import socket
import os
import re
import time
import json

## 执行命令.并将执行结果写入文本
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

## 获取账户余额
def get_money(x):
    cmd = "peer chaincode query -C $CHANNEL_NAME -n mycc -c '{\"Args\":[\"query\",\"%s\"]}'"%x
    result = execCmd(cmd)
    pat1 = ".*Query Result:.*"
    result = re.findall(pat1, result)[0]    # 找到"Query Result:"
    m=re.search("Query Result: ",result)    # 匹配字段
    result=result[:m.start()]+result[m.end():]
    return int(result)

## 获取api调用记录
def get_api(x):
    cmd = "peer chaincode query -C $CHANNEL_NAME -n mycc -c '{\"Args\":[\"query\",\"%s\"]}'" % x
    content = execCmd(cmd)
    pattern = re.compile(r'Query Result:\s([a-zA-Z]+)_([a-zA-Z]+)_(\d+\.\d+\.\d+\.\d+\:\d+)_(\d+)')
    result = re.findall(pattern, content)[0]  # 找到"Query Result:"
    return result[0],result[1],result[2],result[3]
    # return result.group(1),result.group(2),result.group(3),result.group(4)

## 转账函数,self为账户自身,target为转账目标,x为转账金额
def invoke(self,target,x):
    os.system('peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["invoke","%s","%s","%d"]}\'' % (self,target,x))
    time.sleep(3) ## sleep3秒,等待交易确认

def fabric_cloud():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象，用IPv4通信，协议为TCP(family, type)
    ip_port = ('', 2017)  # server的ip一般为空
    s.bind(ip_port)
    s.listen(5)  # 最多连接数
    while True:
        c, addr = s.accept()  # c为新的socket对象，addr为客户的internet地址
        r_data = c.recv(1024).decode()
        r_data = json.loads(r_data)
        invoke(r_data[0], r_data[1], 1) ## 默认转账1
        value=get_value(r_data[0]) ## 得到自身账户value
        c.send(str(value).encode())

if __name__ == "__main__":
    fabric_cloud()

