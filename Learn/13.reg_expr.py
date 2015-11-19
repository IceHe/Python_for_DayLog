#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# re
import re

r = r'^\d{3}\-\d{3,8}$'
print(re.match(r, '010-12345'))
print(re.match(r, '010 12345'))
print()


# split
print('a b   c'.split(' '))
print(re.split(r'\s+', 'a b   c'))
print()

print(re.split(r'[\s\,]+', 'a,b, c  d'))
print(re.split(r'[\s\,\;]+', 'a,b;; c  d'))
print()


# group
m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
print(m)
print(m.group(0))
print(m.group(1))
print(m.group(2))
print()

print(m.groups())
print(m.groups()[0])
print(m.groups()[1])
# print(m.groups()[2]) # error
print()


# greedy
print(re.match(r'^(\d+)(0*)$', '102300').groups())
print()


# compile
re_tel = re.compile(r'^(\d{3})-(\d{3,8})$')
print(re_tel.match('010-12345').groups())
print(re_tel.match('010-8086').groups())
print()
