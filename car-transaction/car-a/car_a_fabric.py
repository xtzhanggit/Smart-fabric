# encoding: utf-8

import os
import re
import time

## 执行命令.并将执行结果写入文本
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

## 获取value,对象为target
def get_value(target):
    cmd = "peer chaincode query -C $CHANNEL_NAME -n mycc -c '{\"Args\":[\"query\",\"%s\"]}'"%target
    result = execCmd(cmd)
    pat1 = ".*Query Result:.*"
    result = re.findall(pat1, result)[0]    # 找到"Query Result:"
    m=re.search("Query Result: ",result)    # 匹配字段
    result=result[:m.start()]+result[m.end():]
    return int(result)

## 转账函数,self为账户自身,target为转账目标,x为转账金额
def invoke(self,target,x):
    os.system('peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["invoke","%s","%s","%d"]}\'' % (self,target,x))
    time.sleep(3) ## sleep3秒,等待交易确认

## 创建新用户函数,target为对象,value为对象初始value
def create(target,value):
    os.system('peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["create","%s","%d"]}\'' % (target,value)) ##添加保险公司账户
    time.sleep(3) ## sleep3秒,等待交易确认
