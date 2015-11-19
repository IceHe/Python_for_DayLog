#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# thread
import time, threading


# threadlocal

# 创建全局ThreadLocal对象：
local_school = threading.local()

def process_student():
    # 获取当前线程关联的student：
    std = local_school.student
    print('Hello, %s (in %s)'
          % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student：
    local_school.student = name
    process_student()

t1 = threading.Thread(target = process_thread,
                      args = ('Alice',),
                      name = 'Thread-A')
t2 = threading.Thread(target = process_thread,
                      args = ('Bob',),
                      name = 'Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
print()


# 新进程执行的代码：
def loop():
    print('thread %s is running...'
          % threading.current_thread().name)
    n = 0
    while n < 3:
        n = n + 1
        print('thread %s >>> %s'
              % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.'
          % threading.current_thread().name)

print('thread %s is running...'
      % threading.current_thread().name)
t = threading.Thread(target = loop, name = 'LoopThread')
t.start()
t.join()
print('thread %s ended.'
      % threading.current_thread().name)
print()


# no lock
balance = 0 # 假设为存款余额

def change_it(n):
    # 先存后取，结果应该为0：
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        change_it(n)

t1 = threading.Thread(target = run_thread, args = (5,))
t2 = threading.Thread(target = run_thread, args = (8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
print()


# lock
balance = 0
lock = threading.Lock()

def run_thread2(n):
    for i in range(100000):
        # 先要获取锁
        lock.acquire()
        try:
            # 此时可放心地修改
            change_it(n)
        finally:
            # 修改完成后必须释放锁
            lock.release()

t1 = threading.Thread(target = run_thread2, args = (5,))
t2 = threading.Thread(target = run_thread2, args = (8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
print()


# cores
import multiprocessing

def loop2():
    x = 0
    while True:
        x = x ^ 1

for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target = loop2)
    t.start()


