#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# map()
def product(x):
    return x * x

print(list(map(product, range(11))))
print()


# reduce()
def add(x, y):
    return x + y

from functools import reduce
print(reduce(add, range(11)))
print()


# map & reduce
def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def c2n(ch):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
                '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[ch]
    return reduce(fn, map(c2n, s))

print(str2int('12345'))
print()

def c2n(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

def s2i(s):
    return reduce(lambda x, y : x * 10 + y, map(c2n, s))

print(s2i('54321'))
print()


# homework: map & reduce
def prod(l):
    def multi(x, y):
        return x * y
    return reduce(multi, l)

print(prod(range(1, 5)))

def format_names(names):
    def proc(name):
        return name[0].upper() + name[1:].lower()
    return map(proc, names)

print(list(format_names(['iCe', 'adam', 'LISA', 'barT'])))
print()


def pd(l):
    return reduce((lambda x, y: x * y), l)

print(pd(range(1, 5)))

def fns(names):
    return map(
        lambda n: n[0].upper() + n[1:].lower(),
        names
    )

print(list(fns(['iCe', 'adam', 'LISA', 'barT'])))
print()

def s2i(str):
    c2i = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    return reduce(
        lambda x, y: x * 10 + y,
        map(lambda ch: c2i[ch], str)
    )

def s2f(s):
    ary = s.split('.')
    l = len(ary[1])
    return s2i(ary[0]) + s2i(ary[1]) / (10 ** l)

print(s2f('123.456'))
print()


# filter
print(list(filter(
    lambda n: n % 2 == 1,
    range(0, 11)
)))
print(list(filter(
    lambda s: s and s.strip(),
    ['A', 'b', '', 'c', None]
)))
print()

# homework: filter
def is_prime(num):
    for x in range(2, int(num ** 0.5) + 1):
        if num % x == 0:
            return False
    return True

print(list(filter(is_prime, range(1, 101))))
print()

def not_prime(n):
    if n == 1:
        return True
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return True
    return False

print(list(filter(not_prime, range(1, 101))))
print()

print('123'[::-1])

def is_palindrome(num):
    return (num == int(str(num)[::-1]))

print(list(filter(is_palindrome, range(1, 1000))))
print()


# sorted
nums = [36, 5, 12, -9, -21]
print(sorted(nums))

# Old for Python2
# def reversed_cmp(x, y):
    # if x > y:
        # return -1
    # elif x < y:
        # return 1
    # else:
        # return 0
# New for Python3
def reversed_cmp(x):
    return -x

print(sorted(nums, key=reversed_cmp))
print(sorted(nums, key=abs))
print()

strs = ['bob', 'about', 'Zoo', 'Credit']
print(sorted(strs))

def cmp_ignore_case(s):
    return s.lower()

print(sorted(strs, key=cmp_ignore_case))
print(sorted(strs, key=str.lower, reverse=True))
print()

# homework: sorted
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

def by_name(t):
    return t[0].lower()

print(sorted(L, key=by_name))

def by_score(t):
    return t[1]

print(sorted(L, key=by_score, reverse=True))
print()


# return function
#def calc_sum(*args):
def calc_sum(args):
    def get_sum():
        sum = 0
        for i in args:
            sum = sum + i
        return sum
    return get_sum

#g = calc_sum(1, 2, 3, 4, 5)
g = calc_sum(range(1, 101))
print(g)
print(g())
print()


# closure
def count():
    fs = []
    for i in range(1, 4):
        def f(j):
            def g():
                return j * j
            return g
        fs.append(f(i))
    return fs

f1, f2, f3 = count()
print(f1(), f2(), f3())
print()

def cnt():
    return map(
        lambda i: (
            lambda : i * i
        ),
        range(1, 4)
    )

#c1, c2, c3 = cnt()
#print(c1(), c2(), c3())
print(cnt())
#print(map(lambda f: f(), cnt()))
print([f() for f in cnt()])
print()

print('Last Test')
y = [(lambda x = i : x * x) for i in range(1, 4)]
print(y)
print([f() for f in y])
print()
