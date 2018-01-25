import re
import subprocess
from datetime import datetime


def execCmd(cmd):
    """
    执行命令.并将执行结果写入文本
    """
    text = subprocess.getoutput(cmd)
    return text


def get_value(x):
    """
    获取账户余额
    """
    cmd = "peer chaincode query -C $CHANNEL_NAME -n mycc -c '{\"Args\":[\"query\",\"%s\"]}'" % x
    result = execCmd(cmd)
    pat1 = ".*Query Result:.*"
    result = re.findall(pat1, result)[0]  # 找到"Query Result:"
    m = re.search("Query Result: ", result)
    result = result[:m.start()] + result[m.end():]  # 删除指定字符窜
    return result


def addAPI(s1, s2, s3):
    """
    添加API
    """
    now_time = datetime.now()
    now_time = now_time.replace(hour=(now_time.hour + 8) % 24)
    cmd='peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["addAPI","%s","%s","%s","%s"]}\'' % (
        now_time, s1, s2, s3)
    execCmd(cmd)


def delete_seconds(s):
    """
    删除时间中的秒数字
    """
    m = re.search(":\d*\.\d*", s)
    result = s[:m.start()] + s[m.end():]
    return result


def get_api_group(x, y):
    """
    获取多个api调用记录
    """
    cmd = "peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c '{\"Args\":[\"testRangeQuery\",\"%s\",\"%s\"]}'" % (
        x, y)
    content = execCmd(cmd)
    pat1 = "Chaincode invoke successful. result: status:200 payload:.*"
    result = re.findall(pat1, content)
    if result == []:
        final_result = "There is no API-call record for this time"
    else:
        final_result=[]
        result = re.findall(pat1, content)[0]
        m = re.search("Chaincode invoke successful. result: status:200 payload:", result)
        result = result[:m.start()] + result[m.end():]  # 删除指定字符窜
        result = result.replace("\"", "")
        result = result.split(",")
        for i in range(10):
            final_result.append(str(delete_seconds(result[len(result)-1-9+i])))
    return final_result


def invoke(self, target, x):
    """
    转账函数,self为账户自身,target为转账目标,x为转账金额
    """
    cmd='peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["invoke","%s","%s","%d"]}\'' % (
            self, target, x)
    execCmd(cmd)


def createKey(target, x):
    """
    创建新用户
    """
    cmd='peer chaincode invoke -o orderer.example.com:7050  --tls $CORE_PEER_TLS_ENABLED --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  -C $CHANNEL_NAME -n mycc -c \'{"Args":["create","%s","%d"]}\'' % (
            target, x)
    execCmd(cmd)
