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
def fabric_local(function,args):
    # flag = judgment(buyer, password) ## 身份验证
    # if 1 == True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_port = ('10.175.152.8', 2017)
    s.connect(ip_port)
    s_data=[]
    s_data.append(function)
    for item in args:
        s_data.append(item)
    json_data=json.dumps(s_data)
    s.send(json_data.encode())
    r_data = s.recv(1024).decode()
    s.close()
    # else:
    #     r_data = "The id or password isn't correct.Please try again."
    return r_data

if __name__ == "__main__":
    # print(fabric_local("addAPI",["2017.11.05.21:15","zxt","xsw","snesor0"]))
    # print(fabric_local("addAPI",["2017.11.05.21:45","zyd","lbq","snesor1"]))
    # print(fabric_local("addAPI",["2017.11.05.22:15","ljo","hxw","snesor2"]))
    # print(fabric_local("addAPI",["2017.11.06.21:15","hzh","sf","snesor3"]))
    # print(fabric_local("addAPI",["2017.12.05.21:15","dxx","ybw","snesor4"]))
    # print(fabric_local("addAPI",["2018.12.05.21:15","xy","sch","snesor5"]))
    print(fabric_local("get_api_group",["2017.11.05.21:15","2018.12.06"]))
    # print(fabric_local("createUser",["c",17]))
    # print(fabric_local("invoke",["a","b",5]))
    # print(fabric_local("get_money",["c"]))
