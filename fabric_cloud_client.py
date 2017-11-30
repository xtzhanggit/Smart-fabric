import socket
import json
import re
from datetime import datetime


"""
客户端程序
"""


def fabric_local(function, args):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_port = ('119.29.241.15', 2017)
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


def api_show():
    now_time = datetime.now()
    foward_time = now_time.replace(hour=(now_time.hour - 1) % 24)
    time_list = [str(foward_time), str(now_time)]
    s = fabric_local("get_api_group", time_list)
    try:
        result = s.replace("\"", "")
        result = result.split(",")
        for item in result:
            item = delete_seconds(item)
            print(item)
    except Exception:
        print("The strings are invalid.")



if __name__ == "__main__":
    # print(fabric_local("addAPI",["zxt","dxx","sensor0"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor1"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor2"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor3"]))
    api_show()
