#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Student(object):
    pass

s = Student()
s.name = 'Ice'
print(s.name)


# bind a function to a instance
def setAge(self, age):
    self.age = age

from types import MethodType
s.set_age = MethodType(setAge, s)
s.set_age(25)
print(s.age)
print()

s2 = Student()
# s2.set_age(25) # error
# print(s2.age) # error


# bind a method to a class
Student.set_age = MethodType(setAge, Student)
s2.set_age(30)
print(s2.age)
print()


# __slots__
class StudentX(object):
    __slots__ = ('name', 'age')

s3 = StudentX()
# s3.gender = 'male' # error
s3.name = 'xxx'
# print(s3.gender) # error
print(s3.name)
print()


# @property
class StudentP(object):
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

s4 = StudentP()
# s4.score = 'abc' # error
# s4.score = 101 # error
# s4.score = -1 # error
s4.score = 99
print(s4.score)
print()


# multiple inheritance & MixIn
class Animal(object):
    def desc(self):
        print("I'm a animal.")

class RunnableMixIn(object):
    def run(self):
        print("I'm running.")

class FlyableMixIn(object):
    def fly(self):
        print("I'm flying.")

class Dog(Animal, RunnableMixIn):
    pass

class Bird(Animal, FlyableMixIn):
    pass

dog = Dog()
dog.desc()
dog.run()
# dog.fly() # error

bird = Bird()
bird.desc()
# bird.run() # error
bird.fly()
print()


# __str__ & __repr__
class StudentD(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Student obj (name: %s)' % self.name

    __repr__ = __str__

print(StudentD('Ice'))
print()


# __iter__ & __getitem__
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 100000:
            raise StopIteration()
        return self.a

    def __getitem__(self, n):
        # a, b = 1, 1
        # for x in range(n):
            # a, b = b, a + b
        # return a
        if isinstance(n, int):
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice):
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L

print([n for n in Fib() if n < 100])
print('Fib()[5] =', Fib()[5])
print('Fib()[5:10] =', Fib()[5:10])
print('Fib()[-5:-10] =', Fib()[-5:-10]) # can't work, need improvement
print()


# __getattr
class StudentA(object):
    def __init__(self, name):
        self.name = name
    def __getattr__(self, attr):
        if attr == 'score':
            return 99
        elif attr == 'age':
            return lambda: 23
        raise AttributeError("'Student' object has no attr '%s'" % attr)

stuA = StudentA('Tes')
print(stuA.name)
print(stuA.score)
print(stuA.age())
# print(stuA.xyz) # error
print()

# chain
class Chain(object):
    def __init__(self, path = ''):
        self.path = path
    def __getattr__(self, path):
        return Chain('%s/%s' % (self.path, path))
    def __str__(self):
        return self.path
    __repr__ = __str__

print(Chain().status.user.timeline.list)


# __call__
class TestCall(object):
    def __init__(self, text = 'default'):
        self.text = text
    def __call__(self):
        print('This is a %s.' % self.text)

t0 = TestCall('test')
t0()
print()

print(callable(TestCall()))
print(callable(t0))
print(callable(t0()))
print()
