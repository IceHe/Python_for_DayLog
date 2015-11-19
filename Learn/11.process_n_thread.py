#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# fork
import os
print('Process (%s) start...' % os.getpid())
# Only works on Unix/Linux/Mac:
pid = os.fork()
if pid == 0:
    print("I'm child proc (%s) and my parentis %s."
          % (os.getpid(), os.getppid()))
else:
    print("I'm (%s) just created a child proc (%s)."
          % (os.getpid(), pid))

print()


# multiprocessing
from multiprocessing import Process

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...'
          % (name, os.getpid()))

if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target = run_proc, args = ('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
