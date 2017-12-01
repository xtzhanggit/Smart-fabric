import os

# 创建通道
os.system('peer channel create -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/channel.tx --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem')

# 加入通道 
os.system('peer channel join -b mychannel.block')

# 更新anchor
os.system('./scripts/script.sh')

# 安装cc
os.system('peer chaincode install -n mycc -v 1.0 -p github.com/hyperledger/fabric/examples/chaincode/go/chaincode_example02')

# 实例化cc
os.system('peer chaincode instantiate -o orderer.example.com:7050 --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C $CHANNEL_NAME -n mycc -v 1.0 -c \'{"Args":["init","a", "100", "b","200"]}\' -P "OR (\'Org1MSP.member\',\'Org2MSP.member\')"')

# 运行server
os.system('python3 ./volumes/fabric_cloud_server.py')
