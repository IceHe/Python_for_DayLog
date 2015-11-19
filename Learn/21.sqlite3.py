#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'


# sqlite
import sqlite3

# will error!
# with sqlite3.connect('test.db') as conn:
#     with conn.cursor() as cursor:
#         cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
#         cursor.execute("insert into user (id, name) values('1', 'Ice')")
#         print(cursor.rowcount)
#         conn.commit()
#
# with sqlite3.connect('test.db') as conn:
#     with conn.cursor() as cursor:
#         cursor.execute('select * from user where id=?', '1')
#         print(cursor.fetchall())

try:
    conn = sqlite3.connect('test.db')
    try:
        cursor = conn.cursor()
        cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
        cursor.execute("insert into user (id, name) values('1', 'Ice')")
        print(cursor.rowcount)
        conn.commit()
    except:
        print('cursor error!')
    finally:
        cursor.close()
except:
    print('conn error!')
finally:
    conn.close()

print()

try:
    conn = sqlite3.connect('test.db')
    try:
        cursor = conn.cursor()
        cursor.execute('select * from user where id=?', '1')
        print(cursor.fetchall())
    except:
        print('cursor error!')
    finally:
        cursor.close()
except:
    print('conn error!')
finally:
    conn.close()

print()


# exercise
import os

db_file = os.path.join(os.path.dirname(__file__), 'test.db')
if os.path.isfile(db_file):
    os.remove(db_file)

# init
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")

cursor.close()
conn.commit()
conn.close()

def get_score_in(low, high):
    try:
        conn = sqlite3.connect(db_file)
        try:
            cursor = conn.cursor()
            cursor.execute(
                'select name from user where score between ? and ? order by score asc',
                (low, high)
            )
            values = cursor.fetchall()

            result = []
            for v in values:
                result.append(v[0])
            print(result)
            return result

            # print([v[0] for v in values])
            # return [v[0] for v in values]

        except:
            print('cursor error')
            return []
        finally:
            cursor.close()

    except:
        print('conn error')
        return []
    finally:
        conn.close()

# test
assert get_score_in(80, 95) == ['Adam']
assert get_score_in(60, 80) == ['Bart', 'Lisa']
assert get_score_in(60, 100) == ['Bart', 'Lisa', 'Adam']

print('Pass')