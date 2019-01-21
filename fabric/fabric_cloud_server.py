import function
import socketserver
import threading
import json

def operate_fabric(r_data):
    """
    操作fabric
    """
    try:
        if r_data[0] == "get_value":
            if len(r_data) == 2:
                result = function.get_value(r_data[1])
            else:
                result = "list index out of range"
        elif r_data[0] == "get_api_group":
            if len(r_data) == 3:
                result = function.get_api_group(r_data[1], r_data[2])
            else:
                result = "list index out of range"
        elif r_data[0] == "invoke":
            if len(r_data) == 4:
                function.invoke(r_data[1], r_data[2], r_data[3])
                result = "The invoke operation has been done."
            else:
                result = "list index out of range"
        elif r_data[0] == "addAPI":
            if len(r_data) == 4:
                function.addAPI(r_data[1], r_data[2], r_data[3])
                result = "The addAPI operation has been done."
            else:
                result = "list index out of range"
        elif r_data[0] == "createKey":
            if len(r_data) == 3:
                function.createKey(r_data[1], r_data[2])
                result = "The createKey operation has been done."
            else:
                result = "list index out of range"
        else:
            result = "No function"
    except Exception:
        result = "The function returns a value error"
    finally:
        return result

class ThreadedTCPRequestHandler(socketserver. BaseRequestHandler):
    """
    监听数据请求
    """
    def handle(self):       # handle方法重载
        data = self.request.recv(1024).decode()
        r_data = json.loads(data)
        s_result = operate_fabric(r_data)
        self.request.sendall(str(s_result).encode())


class ThreadedTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

if __name__=="__main__":

    HOST,PORT='',2017
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST,PORT), ThreadedTCPRequestHandler)
    ip,port = server.server_address

    server_thread = threading.Thread(target = server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    # 使用Ctrl + C退出程序
    server.serve_forever()



