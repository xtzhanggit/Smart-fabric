import socket
import os
import re
import time
import json
import subprocess

# 执行命令.并将执行结果写入文本
def execCmd(cmd):
    text=subprocess.getoutput(cmd)
    return text

# 获取账户余额
def get_value(x):
    cmd = "peer chaincode query -C $CHANNEL_NAME -n mycc -c '{\"Args\":[\"query\",\"%s\"]}'"%x
    result = execCmd(cmd)
    pat1 = ".*Query Result:.*"
    result = re.findall(pat1, result)[0]    # 找到"Query Result:"
    m=re.search("Query Result: ",result)
    result=result[:m.start()]+result[m.end():] # 删除指定字符窜
    return result

# 添加API
def addAPI(s1,s2,s3,s4):
    os.system('peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["addAPI","%s","%s","%s","%s"]}\'' % (s1,s2,s3,s4))
    time.sleep(3)

# # 获取单个api调用记录
# def get_api_element(x):
#     cmd = "peer chaincode query -C $CHANNEL_NAME -n mycc -c '{\"Args\":[\"query\",\"%s\"]}'" % x
#     result = execCmd(cmd)
#     pat1 = ".*Query Result:.*"
#     result = re.findall(pat1, result)[0]  # 找到"Query Result:"
#     m = re.search("Query Result: ", result)
#     result = result[:m.start()] + result[m.end():]  # 删除指定字符窜
#     # return int(result)
#     return result

# 获取多个api调用记录
def get_api_group(x,y):
    cmd = "peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c '{\"Args\":[\"testRangeQuery\",\"%s\",\"%s\"]}'" % (x,y)
    content = execCmd(cmd)
    pat1 = "Chaincode invoke successful. result: status:200 payload:.*"
    result = re.findall(pat1, content)[0]
    m = re.search("Chaincode invoke successful. result: status:200 payload:", result)
    result = result[:m.start()] + result[m.end():]  # 删除指定字符窜
    pat2=","
    result=re.split(pat2,result)
    return result

# 转账函数,self为账户自身,target为转账目标,x为转账金额
def invoke(self,target,x):
    os.system('peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["invoke","%s","%s","%d"]}\'' % (self,target,x))
    time.sleep(3) ## sleep3秒,等待交易确认

# 创建新用户
def createUser(target,x):
    os.system('peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["create","%s","%d"]}\'' % (target,x))
    time.sleep(3)
# def update_api_times(x,y):
#     id=x+"_"+y
#     os.system('peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["updateAPItimes","%s","%s"]}\'' % (x,y))
#     time.sleep(3)
#
# def add_authority(x,rank):
#     id="auth_"+x
#     os.system('peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["create","%s","%d"]}\'' % (id,rank))
#     time.sleep(3)
#
# def get_authority(x):
#     id = "auth_" + x
#     return get_value(id)

def fabric_cloud():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象，用IPv4通信，协议为TCP(family, type)
    ip_port = ('', 2017)  # server的ip一般为空
    s.bind(ip_port)
    s.listen(5)  # 最多连接数
    while True:
        c, addr = s.accept()  # c为新的socket对象，addr为客户的internet地址
        r_data = c.recv(1024).decode()
        r_data = json.loads(r_data)
        if r_data[0]=="get_value":
            result=get_value(r_data[1])
        elif r_data[0]=="get_api_group":
            result=get_api_group(r_data[1],r_data[2])
        elif r_data[0]=="invoke":
            invoke(r_data[1],r_data[2],r_data[3])
            result="The invoke operation has been done."
        elif r_data[0]=="addAPI":
            addAPI(r_data[1],r_data[2],r_data[3],r_data[4])
            result="The addAPI operation has been done."
        else:
            createUser(r_data[1],r_data[2])
            result="The createUser operation has been done."
        c.send(str(result).encode())

if __name__ == "__main__":
    fabric_cloud()