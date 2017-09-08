import socket
import json
import pydb

## 判断用户名和密码是否正确
def judgment(username, password):
    flag=False
    idx, passwordx = pydb.get() ## 账户,密码列表
    for i in range(len(idx)):
        if (idx[i][0] == username) & (passwordx[i][0] == password):
            flag = True
            break
    return flag

## 发送转账信息
def fabric_local(buyer, seller, password):
    flag = judgment(buyer, password) ## 身份验证
    if flag == True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_port = ('119.29.241.15', 2017)
        s.connect(ip_port)
        s_data=[0]*2
        s_data[0]=buyer
        s_data[1]=seller
        json_data=json.dumps(s_data)
        s.send(json_data.encode())
        r_data = s.recv(1024).decode()
        s.close()
    else:
        r_data = "The id or password isn't correct.Please try again."
    return r_data

if __name__ == "__main__":
    result=fabric_local('person2', 'person1', 'person2')
    print(result)
