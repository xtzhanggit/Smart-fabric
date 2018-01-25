import socket
import json
from datetime import datetime
import time

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
        length=(1024**3)*12
        r_data=s.recv(length).decode()
        s.close()
    finally:
        return r_data

"""
展示api
"""


def api_show():
    now_time = datetime.now()
    foward_time = now_time.replace(hour=(now_time.hour - 1) % 24)
    time_list = [str(foward_time), str(now_time)]
    s = fabric_local("get_api_group", time_list)
    print("The last 10 APIs")
    try:
        result = s.split(",")
        for item in result:
            item = item.replace("'","")
            item = item.replace("[","")
            item = item.replace("]","")
            item =item.strip()
            print(item)
    except Exception:
        print(s)
    



if __name__ == "__main__":
    while True:
        print(fabric_local("addAPI",["zxt","dxx","sensor13"]))
        # for i in range(10):
        #    sensor="sensor"+str(i)
        #    print(fabric_local("addAPI",["zxt","unknown",sensor]))
        time.sleep(600)
    # for i in range(500):
    #     print(fabric_local("addAPI", ["zxt", "dxx", "sensor0"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor0"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor1"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor2"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor3"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor4"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor5"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor6"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor7"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor8"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor9"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor10"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor11"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor12"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor13"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor14"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor15"]))
    # print(fabric_local("addAPI",["zxt","dxx","sensor378"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor78"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor521"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor64"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor72"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor8978"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor91"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor104"]))
    # print(fabric_local("addAPI",["zxt", "dxx", "sensor118"]))
    # api_show()
