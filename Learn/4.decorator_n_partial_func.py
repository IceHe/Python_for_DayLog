#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# decorator
def log(func):
    def wrapper(*arg, **kw):
        print("call %s():" % func.__name__)
        return func(*arg, **kw)
    return wrapper

@log
def now():
    print("2015-08-19")

now()
f = now
f()
print(now.__name__)
print(f.__name__)
print()


import functools

def log2(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*arg, **kw):
            print("%s %s():" % (text, func.__name__))
            return func(*arg, **kw)
        return wrapper
    return decorator

@log2('execute')
def now2():
    print("2015-08-20")

now2()
f2 = now2
f2()
print(now2.__name__)
print(f2.__name__)
print()


# homework: decorator
def log3(func):
    @functools.wraps(func)
    def wrapper(*arg, **kw):
        print('begin call')
        rtn = func(*arg, **kw)
        print('end call')
        return rtn
    return wrapper

@log3
def t0():
    print('t0()')

t0()
print(t0.__name__)
print()

def log4(text):
    if callable(text):
        @functools.wraps(text)
        def wrapper(*arg, **kw):
            print('begin call')
            rtn = text(*arg, **kw)
            print('end call')
            return rtn
        return wrapper
    else:
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*arg, **kw):
                print('begin call')
                print('text = %s' % text)
                rtn = func(*arg, **kw)
                print('end call')
                return rtn
            return wrapper
        return decorator


@log4
def t1():
    print('t1()')

@log4('test')
def t2():
    print('t2()')

t1()
print(t1.__name__)
print()

t2()
print(t2.__name__)
print()



# partial function
int2 = functools.partial(int, base=2)
print(int2('1000000'))
print(int2('1111111'))
print()

