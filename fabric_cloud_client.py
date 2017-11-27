import socket
import json
# import pydb

# ## 判断用户名和密码是否正确
# def judgment(username, password):
#     flag=False
#     idx, passwordx = pydb.get() ## 账户,密码列表
#     for i in range(len(idx)):
#         if (idx[i][0] == username) & (passwordx[i][0] == password):
#             flag = True
#             break
#     return flag

## 发送转账信息

"""
客户端程序
"""
def fabric_local(function,args):
    # flag = judgment(buyer, password) ## 身份验证
    # if 1 == True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_port = ('119.29.241.15', 2017)
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
    # print(fabric_local("addAPI",["zxt","dxx","sensor0"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor1"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor2"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor3"]))
    print(fabric_local("get_api_group",["2017-11-11 14:00","2017-11-11 16:00"]))