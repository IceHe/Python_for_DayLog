#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    from datetime import datetime, timedelta
    date_1st = datetime(2015, 10, 1)
    days = 31 + 17
    date_last = date_1st + timedelta(days=days - 1)


    ##############################
    # init DB conn
    ##############################
    import os
    os.system('mysql.server start')

    import pymysql
    conn = pymysql.connect(user='test', password='88887777', database='life_log')
    cursor = conn.cursor()

    sql = r'select date_ymd, oth_data from day_log where date_ymd >= "' \
          + date_1st.strftime('%Y-%m-%d') + '" and date_ymd <= "' \
          + date_last.strftime('%Y-%m-%d') + '"'
    print(sql)

    cursor.execute(sql)
    date_logs = cursor.fetchall()

    cursor.close()
    conn.commit()
    conn.close()

    import json

    for log in date_logs:
        print(log[0])

        data = json.loads(log[1])
        for item in data['discipline']:
            # 以下是分别获得dict的key和value的方法
            for k in item:
                print('\t', k, '= [', item[k], ']')
