#! /usr/bin/python3
# coding=utf-8
from function import *

## 实例化结构体
p1=Person("oppo","xian",7)
os.system('export CHANNEL_NAME=mychannel')
os.system('ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem')
main(p1)
