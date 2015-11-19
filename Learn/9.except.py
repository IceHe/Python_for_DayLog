#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# except & finally
try:
    print('try...')
    r = 10 / 0
    print('result', r)
except ZeroDivisionError as e:
    print('except:', e)
finally:
    print('finally.')
print('ED')
print()

try:
    print('try...')
    r = 10 / int('2')
    print('result:', r)
except ValueError as e:
    print('ValueError:', e)
except ZeroDivisionError as e:
    print('ZeroDivisionError:', e)
else:
    print('no error')
finally:
    print('finally.')
print('ED')

print()


# assert
def foo(s):
    n = int(s)
    assert n != 0, 'n is zero!'
    return 10 / n

# print(foo('0')) # temp comment


# logging
import logging
logging.basicConfig(level=logging.INFO)

import pdb
pdb.set_trace()

s = '0'
n = int(s)
logging.info('n = %d' % n)
print(10 / n)
print()


# unittest
# ...


# doctest
# ...
