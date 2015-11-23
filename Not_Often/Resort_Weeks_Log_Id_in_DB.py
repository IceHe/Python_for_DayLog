#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    import mysql.connector
    conn = mysql.connector.connect(user = 'test', password = '88887777', database='life_log')
    cursor = conn.cursor()

    sql = r'select id, from_date from week_log order by from_date asc'
    cursor.execute(sql)
    days = cursor.fetchall()
    print(days)

    if 0 == len(days):
        print('Error: Can not find any data!')
        exit(1)

    print('total:', len(days), 'days\n')
    print('First Day:', days[0][1])
    print('Last Day:', days[len(days) - 1][1])
    print()

    from datetime import datetime, timedelta

    tmp_id_start = 1000
    for d in days:
        # print(d[0])
        sql = r'update week_log set id = "' + str(tmp_id_start) + r'" where id = "' + str(d[0]) + '"'
        print(sql)
        cursor.execute(sql)
        tmp_id_start += 1

    tmp_id_start = 1000
    new_id_start = 1
    for d in days:
        sql = r'update week_log set id = "' + str(new_id_start) + r'" where id = "' + str(tmp_id_start) + '"'
        print(sql)
        cursor.execute(sql)
        new_id_start += 1
        tmp_id_start += 1

    cursor.close()
    conn.commit()
    conn.close()

