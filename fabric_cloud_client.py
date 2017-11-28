import socket
import json
import re

"""
客户端程序
"""
def fabric_local(function, args):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_port = ('119.29.241.17', 2017)
        s.connect(ip_port)
    except Exception:
        r_data = "The interface is shut down."
    else:
        s_data = []
        s_data.append(function)
        for item in args:
            s_data.append(item)
        json_data = json.dumps(s_data)
        s.send(json_data.encode())
        r_data = s.recv(1024).decode()
        s.close()
    finally:
        return r_data

"""
删除时间中的秒数字
"""
def delete_seconds(s):
    m = re.search(":\d*\.\d*", s)
    result = s[:m.start()] + s[m.end():]
    return result

"""
展示api
"""
def api_show(s):
    result = s.replace("\"", "")
    result = result.split(",")
    for item in result:
        item=delete_seconds(item)
        print(item)



if __name__ == "__main__":
    # print(fabric_local("addAPI",["zxt","sensor0"]))
    # print(fabric_local("addAPI",["zxt","sensor1"]))
    # print(fabric_local("addAPI",["zxt","sensor2"]))
    # print(fabric_local("addAPI",["zxt","sensor3"]))
    result = fabric_local("get_api_group", ["2017-11-27 22:00", "2017-11-27 23:00"])
    api_show(result)

