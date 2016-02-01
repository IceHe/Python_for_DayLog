#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'


# mysql
from Learn import test

conn = test.connector.connect(user ='test', password ='TeSt', database='test')
cursor = conn.cursor()

# cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'Ice'])

print(cursor.rowcount)

conn.commit()
cursor.close()


cursor = conn.cursor()
cursor.execute('select * from user where id = %s', ['1'])
values = cursor.fetchall()

print([v for v in values])

cursor.close()
conn.close()


# sqlalchemy

# import:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类：
Base = declarative_base()

# 定义User对象：
class User(Base):
    __tablename__ = 'user'

    id = Column(String(20), primary_key = True)
    name = Column(String(20))

engine = create_engine('mysql+mysqlconnector://test:TeSt@localhost:3306/test')
DBSession = sessionmaker(bind = engine)

session = DBSession()

new_user = User(id = '5', name = 'Bob')
session.add(new_user)
session.commit()
session.close()


session = DBSession()
user = session.query(User).filter(User.id == '5').one()

print('type:', type(user))
print('name:', user.name)

session.close()
