#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'


# udp
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 9999))

print('Bind UDP on 9999')
while True:
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s.' % addr)
    # s.sendto(b'Hello, %s!' % data, addr)
    #  b'%s' % str 在Python3.5会支持，但3.4不支持
    s.sendto(bytes('Hello, %s!' % data, 'utf-8'), addr)
