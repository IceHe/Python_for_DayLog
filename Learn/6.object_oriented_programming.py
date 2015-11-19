#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# class
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))


bart = Student('Bart', 59)
lisa = Student('Lisa', 87)
bart.print_score()
lisa.print_score()
print()

print(bart._Student__name)
print(lisa._Student__score)
print()

# print(bart.__name)
# print(lisa.__score)


# inheritance
class Animal(object):
    def run(self):
        print('Animal is running...')

class Dog(Animal):
    def run(self):
        print('Dog is running...')

class Cat(Animal):
    def run(self):
        print('Cat is running...')

animal = Animal()
dog = Dog()
cat = Cat()

animal.run()
dog.run()
cat.run()
print()

print(isinstance(animal, Animal))
print(isinstance(animal, Dog))
print(isinstance(animal, Cat))
print()

print(isinstance(dog, Animal))
print(isinstance(dog, Dog))
print(isinstance(dog, Cat))
print()

print(isinstance(cat, Animal))
print(isinstance(cat, Dog))
print(isinstance(cat, Cat))
print()


# polymorphism
def run_twice(animal):
    animal.run()
    animal.run()

run_twice(animal)
run_twice(dog)
run_twice(cat)
print()


# data type
print(type(123))
print(type(3.14))
print(type('str'))
print(type(True))
print(type(None))
print(type(abs))
print(type(run_twice))
print(type(animal))
print(type(dog))
print()

print(type(123) == type(456))
print(type(123) == int)
print(type('abc') == type('def'))
print(type('abc') == str)
print(type([]) == list)
print(type(str) == type)
print()

print(type('abc') == type(123))
print(type(None) == None)
print()

import types
print(type(run_twice) == types.FunctionType)
print(type(abs) == types.BuiltinFunctionType)
print(type(lambda x: x) == types.LambdaType)
print(type((x for x in range(10))) == types.GeneratorType)
print()


# dir()
print(dir('ABC'))
print()

class MyDog(object):
    def __len__(self):
        return 100

myDog = MyDog()
print(len(myDog))
print(myDog.__len__())


# getattr & setattr & hasattr
class MyObj(object):
    def __init__(self):
        self.x = 9
    def power(self):
        return self.x * self.x

obj = MyObj()
print(hasattr(obj, 'x'))
print(obj.x)
print(hasattr(obj, 'y'))
setattr(obj, 'y', 19)
print(hasattr(obj, 'y'))
print(getattr(obj, 'y'))
print(obj.y)
# print(getattr(obj, 'z'))
print(getattr(obj, 'z', 404))
print()


# class's attribute
class ClsAttr(object):
    name = 'TestClsAttr'

class ClsSon(ClsAttr):
    pass

print(ClsAttr.name)
cs = ClsSon()
print(cs.name)
cs.name = 'Changed Name'
print(cs.name)
print()
