import socket
import json
from datetime import datetime


def process_message(function, args):
    """
    处理发送信息
    """
    s_data = []
    s_data.append(function)
    for item in args:
        s_data.append(item)
    json_data = json.dumps(s_data)
    return json_data


def client(ip, port ,message):
    """
    客户端程序
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
    except Exception:
        response = "The interface is shut down"
    else:
        s.sendall(message.encode())
        response = s.recv(1024).decode()
        s.close()
    return response


def send_recv(function, args, ip, port):
    """
    向fabric发送消息,并接收反馈
    """
    message = process_message(function, args)
    response = client(ip, port, message)
    return response


def api_show(ip, port):
    """
    展示api调用记录
    """
    now_time = datetime.now()
    foward_time = now_time.replace(hour=(now_time.hour - 1) % 24)
    time_list = [str(foward_time), str(now_time)]
    response = send_recv("get_api_group", time_list, ip, port)
    print("The last 10 APIs")
    try:
        result = response.split(",")
        for item in result:
            item = item.replace("'", "")
            item = item.replace("[", "")
            item = item.replace("]", "")
            item = item.strip()
            print(item)
    except Exception:
        print(response)



if __name__=="__main__":
    ip, port = '119.29.241.15', 2017
    # for i in range(10):
    #     print(send_recv("addAPI", ["zxt", "dxx", "sensor0"], ip, port))
    # print(send_recv("addAPI",["zxt","dxx","sensor0"], ip, port))
    # print(send_recv("addAPI",["zxt","dxx","sensor1"], ip, port))
    # print(send_recv("addAPI",["zxt","dxx","sensor2"], ip, port))
    # print(send_recv("addAPI",["zxt","dxx","sensor3"], ip, port))
    # print(send_recv("addAPI",["zxt", "dxx", "sensor4"], ip, port))
    # print(send_recv("addAPI",["zxt", "dxx", "sensor5"], ip, port))
    # print(send_recv("addAPI",["zxt", "dxx", "sensor6"], ip, port))
    # print(send_recv("addAPI",["zxt", "dxx", "sensor7"], ip, port))
    # print(send_recv("addAPI",["zxt", "dxx", "sensor8"], ip, port))
    # print(send_recv("addAPI",["zxt", "dxx", "sensor9"], ip, port))
    # print(send_recv("addAPI",["zxt", "dxx", "sensor10"], ip, port))
    api_show(ip, port)

