#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'


# test server
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

# 接收欢迎信息：
print(s.recv(1024).decode('utf-8'))
for data in [b'Micheal', b'Tracy', b'Sarah']:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()
