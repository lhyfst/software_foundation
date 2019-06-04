# -*- coding: utf-8 -*-

"""Using a Semaphore to synchronize threads"""
import threading
import time
import random

# The optional argument gives the initial value for the internal
# counter;
# it defaults to 1.
# If the value given is less than 0, ValueError is raised.
offer1 = threading.Semaphore(0)  # 定义信号量对应烟草和纸组合的资源
offer2 = threading.Semaphore(0)  # 定义信号量对应烟草和胶水组合的资源
offer3 = threading.Semaphore(0)  # 定义信号量对应纸和胶水组合的资源
finish = threading.Semaphore(0)  # 定义信号量表示抽烟是否完成
# semaphore = threading.Semaphore(0)

def smoker_1():
    name = "smoker_1"
    objects = "烟草和纸"
#     while True:
    for _ in range(10):
        print name + " is waiting."
        offer1.acquire()
        print name + " 拿 " + objects
        tmp_time = random.random()*3
        time.sleep(tmp_time)
        print name + "卷成烟，抽掉"
        # The consumer have access to the shared resource
        print name + " 需 " + objects
        finish.release()
    
def smoker_2():
    name = "smoker_2"
    objects = "烟草和胶水"
#     while True:
    for _ in range(10):
        print name + " is waiting."
        offer2.acquire()
        print name + " 拿 " + objects
        tmp_time = random.random()*3
        time.sleep(tmp_time)
        print name + "卷成烟，抽掉"
        # The consumer have access to the shared resource
        print name + " 需 " + objects
        finish.release()
        
def smoker_3():
    name = "smoker_3"
    objects = "纸和胶水"
#     while True:
    for _ in range(10):
        print name + " is waiting."
        offer3.acquire()
        print name + " 拿 " + objects
        tmp_time = random.random()*3
        time.sleep(tmp_time)
        print name + "卷成烟，抽掉"
        # The consumer have access to the shared resource
        print name + " 需 " + objects
        finish.release()
        
def server():
#     while True:
    for _ in range(15):
        global item
        time.sleep(2)
        # create a random item
        item = random.randint(0, 1000) % 3
        if item == 0:
            print "供应者 %s 给 smoker_1 提供了烟草和纸" % threading.current_thread().name
            offer1.release()
        elif item == 1:
            print "供应者 %s 给 smoker_2 提供了烟草和胶水" % threading.current_thread().name
            offer2.release()
        else:
            print "供应者 %s 给 smoker_3 提供了纸和胶水" % threading.current_thread().name
            offer3.release()
        finish.acquire()


if __name__ == '__main__':
#     for i in range (0,5) :
    smoker_1 = threading.Thread(target=smoker_1)
    smoker_2 = threading.Thread(target=smoker_2)
    smoker_3 = threading.Thread(target=smoker_3)
    server_1 = threading.Thread(target=server,name='server_1')
    server_2 = threading.Thread(target=server,name='server_2')

    smoker_1.setDaemon(True)
    smoker_2.setDaemon(True)
    smoker_3.setDaemon(True)
    server_1.setDaemon(True)
    server_2.setDaemon(True)
    
    smoker_1.start()
    smoker_2.start()
    smoker_3.start()
    server_1.start()
    server_2.start()

    smoker_1.join()
    smoker_2.join()
    smoker_3.join()
    server_1.join()
    server_2.join()
        
    print("program terminated")
