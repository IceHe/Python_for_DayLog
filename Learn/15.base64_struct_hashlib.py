#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'


# base64
import base64
print(base64.b64encode(b'binary\x00string'))
print(base64.b64decode(b'YmluYXJ5AHN0cmluZw=='))
print()

print(base64.b64encode(b'i\xb7\x1d\xfb\xef\xff'))
print(base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff'))
print(base64.urlsafe_b64decode('abcd--__'))
print()


# struct
n = 10240099
b1 = (n & 0xff000000) >> 24
b2 = (n & 0xff0000) >> 16
b3 = (n & 0xff00) >> 8
b4 = (n & 0xff)
bs = bytes([b1, b2, b3, b4])
print(bs)
print()

import struct
print(struct.pack('>I', 10240099))
print()

print(struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80'))
print()


# hashlib
import hashlib
md5 = hashlib.md5()
md5.update('how to use md5 in '.encode('utf-8'))
md5.update('python hashlib?'.encode('utf-8'))
print(md5.hexdigest())
print()

sha1 = hashlib.sha1()
sha1.update('how to use sha1 in '.encode('utf-8'))
sha1.update('python hashlib?'.encode('utf-8'))
print(sha1.hexdigest())
print()
