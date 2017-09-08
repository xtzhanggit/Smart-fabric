# encoding: utf-8

from car_a_function import *
from car_a_client import *
from car_a_server import *
from depth import *

def main(weight,percentage):  ## weight为初始订购件数,percentage为预付百分比
    
    ## 检查水位是否低于标准线
    while True:
        a = Depth('waterSensorv2.0', 'host_remote')
        depthx = a.getDepth()
        print("The depth of water is:%f"%(float(depthx)))
        if float(depthx)<100:
            break
    print("\033[1;31;47mThe initial value is:%d\033[0m"%get_value('a')) ## 得到a的初始值
    
    
    ## 询问卖家货源是否充足,得到成交件数
    #port=1025  ## 初始通信端口
    #number,text=a_order_ask(weight,port) ## number为0代表货源不足,为1代表货源充足;text为卖家反馈信息
    #while True:
    #    if number != 1:   ## 货源不足的处理
    #        print(text+'\n') ## 打印卖家反馈信息
    #        port+=1 ## 下次通信端口+1,避免堵塞
    #        weight=int(weight*0.5) ## 订购份数减半,并转化为Int型
    #        time.sleep(3) ## 隔3秒进行下一次询问
    #        number,text=a_order_ask(weight,port) ## 下一次询问
    #    else : ## 货源充足处理
    #        print(text+'\n')
    #        break ## 退出循环

    a_order(weight,percentage) ## a发起订单,向卖家转预付金,买东西

    a_receive_wait() ## 等待b发车通知

    a_take_delivery(weight, percentage) ## a等待收货


if __name__ == "__main__":
    main(10,0.2)
