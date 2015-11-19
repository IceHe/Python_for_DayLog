#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    f = open('./t_f0.txt', 'r')
    print(f.read())
finally:
    if f:
        f.close()


# with
# auto call f.close()
with open('./t_f0.txt', 'r') as f:
    print(f.read())


# readline
with open('./t_f1.txt', 'r') as f:
    for line in f.readlines():
        print(line.strip()) # rm '\n' at the eol
print()


# binary file
with open('./t_f0.txt', 'rb') as f:
    print(f.read())
print()


# encoding
with open('./t_f2.txt', 'r', encoding='gbk') as f:
    print(f.read())


# write
with open('./t_f3.txt', 'w') as f:
    f.write('test write~')
with open('./t_f3.txt', 'r') as f:
    print(f.read())
print()


# StringIO
from io import StringIO
f = StringIO()
f.write('hello')
f.write(' ')
f.write('world!')
print(f.getvalue())
print()

f = StringIO('Hello!\nHi!\nGoodbye!')
while True:
    s = f.readline()
    if s == '':
        break
    print(s.strip())
print()


# BytesIO
from io import BytesIO
f = BytesIO()
f.write('中文'.encode('utf-8'))
print(f.getvalue())
print()


# os
import os
print(os.name)
print()
print(os.uname())
print()
print(os.environ)
print()
print(os.environ.get('USER'))
print()
print(os.environ.get('x', 'default'))
print()

print(os.path.abspath('.'))
print(os.path.join('.', 'testdir'))
print()

os.mkdir(os.path.join('.', 'testdir'))
os.rmdir(os.path.join('.', 'testdir'))

print(os.path.split(str(os.path.abspath('./t_f0.txt'))))
print(os.path.splitext(str(os.path.abspath('./t_f0.txt'))))
print()

os.rename('t_f4.txt', 'a_f.txt')
os.rename('a_f.txt', 't_f4.txt')
# os.remove('a_f.txt')

print([x for x in os.listdir('.') if os.path.isdir(x)])
print([x for x in os.listdir('.')
        if os.path.isfile(x)
            and os.path.splitext(x)[1] == '.py'])
print()


# serialization
import pickle
d = dict(name='Bob', age=20, score=88)
print(pickle.dumps(d))
print()

with open('dump.txt', 'wb') as f:
    pickle.dump(d, f)
print()

with open('dump.txt', 'rb') as f:
    print(pickle.load(f))
print()


# json
import json
print(json.dumps(d))
print()

json_str = '{"age": 20, "score":88, "name": "Bob"}'
print('json.loads(str) = ', json.loads(json_str))
print()


# advanced json
class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Bob', 20, 88)
# print(json.dumps(s)) # error

def stu2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }

print(json.dumps(s, default = stu2dict))
print()

def dict2stu(d):
    return Student(d['name'], d['age'], d['score'])
print(json.loads(
     json.dumps(s, default = stu2dict),
    object_hook = dict2stu
))
