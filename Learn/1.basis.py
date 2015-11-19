#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print('hello world')
# This's a comment.
print()

print('''line1 hzy
line2 haha
line3 ice''')
print()

print(r'a\tb\nc')
print()

T = True
F = False
print(T)
print(F)
print(T and F)
print(T or F)
print(not T)
print(not F)
print(None)
print()

a = 'x'
b = a
a = 'y'
print('a =', a)
print('b =', b)
print()

print('10 / 3 = ', 10 / 3)
print('10.0 / 3 = ', 10.0 / 3)
print('10 // 3 = ', 10 // 3)
print('10.0 // 3 = ', 10.0 // 3)
print('10 % 3 = ', 10 % 4)
print()

print('ord(\'A\') = ', ord('A'))
print('chr(65) = ', chr(65))
print()

print(u'中文')
# print('这是中文')
print()

print('Hello, I\'m %s!' % 'Ice He')
print('My age is %d' %  23.1)
print('My height is %.2f.' %  162.5)
print('My PWD is %x' % 250)
print('haha %d, %s' % (12, 'nothing'))
print()

list1 = ['Ace', 'Bob', 'Cat']
print('list1 =', list1)
print('list1[0] = ', list1[0])
print('list1[1] = ', list1[1])
print('list1[2] = ', list1[2])
# print('list1[3] = ', list1[3])
print('list1[-1] = ', list1[-1])
print('list1[-2] = ', list1[-2])
print('list1[-3] = ', list1[-3])
# print('list1[-4] = ', list1[-4])
print('len(list1) =', len(list1))
print()

print(range(5))
print()

tuple1 = (2,)
tuple2 = (1, 3, 5)
print('1 elem tuple  = ', tuple1)
print('3 elems tuple = ', tuple2)
print()

#age = int(raw_input('Your age:'))
age = 16
if age < 14:
    print('child')
elif age < 18:
    print('teenager')
else:
    print('adult')
print()

for i in range(5):
    print('i = ', i)
print()

i = 0
while i < 5:
    print('i = ', i)
    i += 1
print()

dict = {'Ace': 5, 'Ice': 23, 'He': 14}
print('dict = ', dict)
print('dict[\'Ace\'] = ', dict['Ace'])
#print('dict[\'Bob\'] = ', dict['Bob'])
print()

print('Bob' in dict)
print('He' in dict)
print(dict.get('Ice'))
print(dict.get('Cat'))
print()

s = set([1, 5, 7])
print(s)
s.add('abc')
print(s)
s.remove(5)
print(s)
s.add((1,))
print(s)
s.add(('abc', 65, 12.2, u'哈哈'))
print(s)
print()

print(int('123'))
print(int(12.34))
print(float('66.2'))
print(float(99))
print(str(810))
print(str(9.11))
print(333)
print(bool(10))
print(bool(0))
print(bool(''))
print(bool('abc'))
print()

def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x

print(my_abs(-0.1))
print()

def swap(a, b):
    if a > b:
        pass
    return b, a

print(swap(1, 2))
ra, rb = swap(1, 2)
print(ra)
print(rb)
print()


# default parameters
def add_end(L = []):
    L.append('END')
    return L

print(add_end())
print(add_end())
print(add_end())
print()

def add_ed(L = None):
    if L == None:
        L = []
    L.append('END')
    return L

print(add_ed())
print(add_ed())
print(add_ed())
print()


# variadic parameter
def cals(*nums):
    sum = 0
    for x in nums:
        sum += x
    return sum

#print(cals(range(8)))
print(cals(*range(101)))
print(cals(1, 2, 3))
print(cals(1, 2, 3, 4, 5))
print()


# keyword parameter
def t_kw_param1(x, y, **kw):
    print(x, y)
    print('*kw', kw)
    print()

def t_kw_param2(x, y, *, a = 'ice', b):
    print(x, y)
    print(a, b)
    print()

kw = {'a': 'aha', 'b': 'hehe'}
t_kw_param1(1, 'y', a = 'he', b = 'bob')
t_kw_param1(1, 'y', b = 'boy')
t_kw_param1(1, 'y')
t_kw_param2(2, 'Y', b = 'B')
t_kw_param2(2, 'Y', a = 'A', b = 'must')
print()


# all parameter test
def t_param1(a, b=0, *args, **kw):
    print('a =', a, 'b =', b,
          '*arg =', args, '**kw =', kw)
    print()

def t_param2(a, b=0, *, x, y='Y', **kw):
    print('a =', a, 'b =', b,
          'x =', x, 'y =', y, '**kw =', kw)
    print()

t_y = 'hi'

t_param1(65)
t_param1(66, 'B')
t_param1(66, 'B', 1, '2', '3c', x='XX', y=t_y, oth='OTH', kwed='ed.')
t_param2(67, 'BB', x='XX', oth='OTH', kwed='ed.')
t_param2(67, 'BB', x='XX', y=t_y, oth='OTH', kwed='ed.')

