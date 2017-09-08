# encoding: utf-8

from car_b_function import *
from car_b_server import *
from car_b_client import *
from multiprocessing import Process

## percentage为预付金额en百分比
def b_main(percentage):
    create('c',100) ## 初始化保险公司
    b_value1 = get_value('b')  ## b的value初始值
    print("\033[1;31;47mThe initial value is:%d \033[0m" % b_value1)
    
    #weight=b_receive_wait() ## 检验订单是否符合条件,返回最后符合要求的订单份数
    #print("The order quantity is %d"% weight)
    b_value2=b_receive_order(10, percentage, b_value1) ## b收到订金后,向c买保险,b_value2为收到预付款后的账户余额
    b_inform_a() ## 通知a小车出发

    pb=Process(target=b_wait_information,args=(10, percentage, b_value2)) ## b等待收货通知进程
    pcar=Process(target=start_car,args=()) ## 发车进程
    pb.start()
    pcar.start()


b_main(0.2)

