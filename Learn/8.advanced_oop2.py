#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# enumeration class
from enum import Enum
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

print([x for x in Month])
print()

from enum import unique

@unique
class Weekday(Enum):
    Sun = 0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

print([x for x in Weekday])
print()

print(Weekday.Mon)
print(Weekday(2))
print(Weekday['Wed'])
print(Weekday.Mon.value)
print(Weekday(2).value)
print(Weekday['Wed'].value)
# print(Weekday[4]) # error
print()


# declare class dynamically using type()
def fn(self, name = 'world'):
    print('Hello, %s.' % name)

Hello = type('Hello', (object,), dict(hello = fn))
h = Hello()
h.hello()
print(type(h))
print(type(Hello))
print()


# metaclass
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, val: self.append(val)
        return type.__new__(cls, name, bases, attrs)

class MyList(list, metaclass = ListMetaclass):
    pass

L = MyList()
L.add(1)
L.add(2)
L.add(3)
print(L)


# ORM
class Field(object):
    def __init__(self, name, col_type):
        self.name = name
        self.col_type = col_type
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

class IntField(Field):
    def __init__(self, name):
        super(IntField, self).__init__(name, 'bigint')

class StrField(Field):
    def __init__(self, name):
        super(StrField, self).__init__(name, 'varchar(100)')

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass = ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value
    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

class User(Model):
    id = IntField('ID')
    name = StrField('UserName')
    email = StrField('Email')
    pwd = StrField('Pwd')

u = User(id = 11, name = 'Ice', email = 'ice_he@foxmail.com', pwd='123')
u.save()


