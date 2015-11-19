#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Ice He'

w_kg = 55.6
w_jin = w_kg * 2

h_cm = 163
age = 23

calorie = 655.096+ 9.563 * w_kg + 1.85 * h_cm - 4.676 * 23

for x in range(10, 16):
    print(w_jin * x)
print()

print('基础热量：', calorie)
print()

