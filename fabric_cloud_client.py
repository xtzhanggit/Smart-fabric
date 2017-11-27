import socket
import json

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


def api_show(s):
    result = s.replace("\"", "")
    result = result.split(",")
    for item in result:
        print(item)


if __name__ == "__main__":
    # fabric_local("addAPI",["zxt","dxx","sensor0"])
    # fabric_local("addAPI",["zxt","dxx","sensor1"])
    # fabric_local("addAPI",["zxt","dxx","sensor2"])
    # fabric_local("addAPI",["zxt","dxx","sensor3"])
    result = fabric_local("get_api_group", ["2017-11-27 16:00", "2017-11-27 16:30"])
    api_show(result)
