import os
import re
import socket
import json
import time


## 执行命令.并将执行结果写入文本
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

## 获取value
def get_value(x):
    #if __name__ == '__main__':
    cmd = "peer chaincode query -C $CHANNEL_NAME -n mycc -c '{\"Args\":[\"query\",\"%s\"]}'"%x
    result = execCmd(cmd)
    pat1 = ".*Query Result:.*"
    result = re.findall(pat1, result)[0]    # 找到"Query Result:"
    m=re.search("Query Result: ",result)    # 匹配字段
    result=result[:m.start()]+result[m.end():]
    return int(result)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
ip_port = ('192.168.1.10', 1375)  # 局域网server的ip，公共端口号
s.connect(ip_port)
data=[0]*3
while True:
    data[0]=get_value('a')
    data[1] = get_value('b')
    data[2] = get_value('c')
    json_data=json.dumps(data)
    s.send(json_data.encode())


    

