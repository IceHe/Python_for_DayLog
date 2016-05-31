#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    import pymysql
    conn = pymysql.connect(user='test', password='88887777', database='life_log')
    cursor = conn.cursor()

    sql = r'select date_ymd from day_log order by date_ymd asc'
    cursor.execute(sql)
    days = cursor.fetchall()

    if 0 == len(days):
        print('Error: Can not find any data!')
        exit(1)

    print('total:', len(days), 'days\n')
    print('First Day:', days[0][0])
    print('Last Day:', days[len(days) - 1][0])
    print()

    from datetime import datetime, timedelta

    error_cnt = 0
    prev_day = days[0][0] - timedelta(days=1)
    for d in days:
        if d[0] != (prev_day + timedelta(days=1)):
            error_cnt += 1
            print('Error', error_cnt, ':', d[0])
        prev_day = d[0]

    cursor.close()
    conn.commit()
    conn.close()

    if error_cnt > 0:
        print(error_cnt, 'errors!')
        exit(1)
    else:
        print('No error ~')
