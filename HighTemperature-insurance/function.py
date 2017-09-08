#! /usr/bin/python3
# coding=utf-8
from struct import *
import os
import time
import hfv

#  main函数
def main(p):
    insurance(p)
    earnings(p)

## 投保函数
def insurance(p):
    if p.city=="beijing":
        insurance_bj(p)
    elif p.city=="hangzhou":
        insurance_hz(p)
    elif p.city=="xian":
        insurance_xa(p)

# 收益函数
def earnings(p):
    if p.city=="beijing":
        earnings_bj(p)
    elif p.city=="hangzhou":
        earnings_hz(p)
    elif p.city=="xian":
        earnings_xa(p)
        
## 北京投保函数
def insurance_bj(p):
    if 35>30: ## 获取温度
        create(p)
        time.sleep(3)
        buy(p)
    
## 杭州投保函数
def insurance_hz(p):
    if 35>32: ## 获取温度
        create(p)
        time.sleep(3)
        buy(p)

## 西安投保函数
def insurance_xa(p):
    if 40>35: ## 获取温度
        create(p)
        time.sleep(3)
        buy(p)

## 北京收益函数
def earnings_bj(p):
    i=0 ## 累积高温天数
    earn_sum=0 ## 累积返保
    while True:
        if 40>37:
            i+=1
            if (i>6) : ## 累积第七天开始返保
                if earn_sum < (100 * p.number+0.1): ## 返保上限为5*份数
                    single_earn(p)
                    time.sleep(3)
                    earn_sum+=5*p.number
                else:
                    break
            else :
                print("mianpeiweijieshu")
        else:
            print("weidadaoyuzhi")


## 杭州收益函数
def earnings_hz(p):
    i = 0  ## 累积高温天数
    earn_sum = 0  ## 累积返保
    while True:
        if 40 > 37:
            i += 1
            if (i > 25):  ## 累积第26天开始返保
                if earn_sum < (100 * p.number+0.1):  ## 返保上限为5*份数
                    single_earn(p)
                    time.sleep(3)
                    earn_sum += 5 * p.number
                else:
                    break
            else:
                print("mianpeiweijieshu")
        else:
            print("weidadaoyuzhi")

## 西安收益函数
def earnings_xa(p):
    i = 0  ## 累积高温天数
    earn_sum = 0  ## 累积返保
    while True:
        if 40 > 37:
            i += 1
            if (i > 12):  ## 累积第13天开始返保
                if earn_sum < (100 * p.number+0.1):  ## 返保上限为5*份数
                    single_earn(p)
                    time.sleep(3)
                    earn_sum += 5 * p.number
                else:
                    break
            else:
                print("mianpeiweijieshu")
        else:
            print("weidadaoyuzhi")

# 获取温度函数
def gettemp():
    while True:
        time.sleep(5)
        (x, y) = hfv.dht11_temp_humi('dht11v2.0', 'docker_remote')  # x为温度,y为湿度
        x = float(x)
        y = float(y)
        print("The tempreture is: %f" % x + '\n' + "The humidity is: %f" % y)
        err = "The trade is not vaild!"
        break
    return x   ## 返回温度


## 创建新用户
def create(p):
    os.system(
        'peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["create","%s","100"]}\'' % p.name)

## 投保
def buy(p):
    money = p.number * 10
    os.system(
        'peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["invoke","%s","IC","%d"]}\'' % (
        p.name, money))

## 单日返保
def single_earn(p):
    money = p.number * 5
    os.system(
        'peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["invoke","IC","%s","%d"]}\'' % (
            p.name, money))
