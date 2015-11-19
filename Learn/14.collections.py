#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

# collections
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p)
print(p.x)
print(p.y)
print()

Point2 = namedtuple('Point2', ('x', 'y'))
p2 = Point2(1, 2)
print(p2)
print(p2.x)
print(p2.y)
print()

print(isinstance(p, Point))
print(isinstance(p, tuple))
print()


# deque
from collections import deque
q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print(q)
print()


# defaultdict
from collections import defaultdict
dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
print(dd['key1'])
print(dd['key2'])
print()


# OrderedDict
from collections import OrderedDict
d = dict([('a', 1), ('b', 2), ('c', 3)])
print(d)

od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print(od)
print()

od2 = OrderedDict()
od2['b'] = 1
od2['a'] = 2
od2['d'] = 3
print(od2)
print()

class LastUpdateOrderedDict(OrderedDict):
    def __init__(self, capacity):
        super(LastUpdateOrderedDict, self).__init__()
        self.capacity = capacity
    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last = False)
            print('remove:', last)
        if containsKey:
            del self[key]
            print('set:', (key, value))
        else:
            print('add:', (key, value))
        OrderedDict.__setitem__(self, key, value)


# Counter
from collections import Counter
c = Counter()
for ch in 'programming':
    c[ch] = c[ch] + 1
print(c)
print()
