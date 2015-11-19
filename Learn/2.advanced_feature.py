#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 切片！Slice
L = ['Ice', 'Bob', 'Cat', 'Foo', 'Bar']
print(L)
print(L[0:3])
print(L[:3])
print(L[3:4])
print(L[-1:])
print(L[-4:-2])
print()

LA = range(100)
print(LA[:10]) # first ten
print(LA[-10:]) # last ten
print(LA[45:55]) # mid ten
print(LA[70:-20]) # test
print()

print(LA[::5]) # step = 5
print(LA[:10:2]) # step = 2
print(LA[:30:3]) # step = 3
print(L[:]) # Copy L!
print()

# tuple's slice is slice
T = (0, 1, 2, 3, 4)
print(T[:3])
print(T[-2:])
print()

Str = r'abc\t\n\r'
print(Str[:5])
print(Str[-6::2])
print(Str[-7::2])
print()


# Iterator 迭代
dict = {'Ace': 5, 'Ice': 23, 'He': 14}

# 默认迭代dict的key
for key in dict:
    print(key, '=', dict[key])
print()


# Python2: 使用 dict.itervalues() 遍历dict的value
#          使用 enumerate( ... ) 同时遍历key与value
# for val in dict.itervalues():
    # print(val)
# for k, v in enumerate(dict):
    # print(k, ' = ', v)

# Python3: 如果要迭代value，用d.values()
#          如果要同时迭代key和value，用d.items()
for v in dict.values():
    print(v)
print()
for k, v in dict.items():
    print(k, '=', v)
print()

# 同时引用两个变量
for x, y in [(1, 1), (2, 4), (3, 9)]:
    print('%s, %s' % (x, y))
print()

# 还可以遍历字符串的字母
for ch in 'IceHe':
    print(ch)
print()

# 判断一个对象是否可迭代访问
from collections import Iterable
print(isinstance('abc', Iterable))
print(isinstance([1, 2, 3], Iterable))
print(isinstance((4, 5, 'abc'), Iterable))
print(isinstance({'a': 1, 'b': 4, 'ef': 23.5}, Iterable))
print(isinstance(123, Iterable))
print()

# Python内置的enumerate函数可以把一个list变成索引-元素对
# 就可以在for循环中同事迭代索引和元素本身
for k, v in enumerate(range(5)):
    print(k, '=', v)
print()
for k, v in enumerate('IceHe'):
    print(k, '=', v)
print()


# List Comprehensions
print([x * x for x in range(1, 10)])
print([x for x in range(1, 10) if x % 3 == 0])
print([(x, y) for x in range(4, 7) for y in range(1, 4)])
import os
print([d for d in os.listdir('.')])
print()


# Generator
generator = (x * x for x in range(1, 10))
for n in generator:
    print(n)
print()

def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1

fib_g = fib(6)
print(next(fib_g))
print(next(fib_g))
print(next(fib_g))
print(next(fib_g))
print(next(fib_g))
print(next(fib_g))
# print(next(fib_g)) # will Error
print()


# Iterator
from collections import Iterable
print(isinstance([], Iterable))
print(isinstance({}, Iterable))
print(isinstance('abc', Iterable))
print(isinstance(range(10), Iterable))
print(isinstance([x for x in range(10)], Iterable))
print(isinstance((x for x in range(10)), Iterable))
print(isinstance(100, Iterable))
print()

from collections import Iterator
print(isinstance([], Iterator))
print(isinstance({}, Iterator))
print(isinstance('abc', Iterator))
print(isinstance(range(10), Iterator))
print(isinstance([x for x in range(10)], Iterator))
print(isinstance((x for x in range(10)), Iterator))
print(isinstance(100, Iterator))
print()
