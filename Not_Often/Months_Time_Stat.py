#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    from datetime import datetime, timedelta
    specified_day = datetime(2015, 1, 1)

    # {datetime}.weekday() == 0 表示 周一
    if 1 != specified_day.day:
        print('It isn\'t 1st day of the new month!')
        exit(1)

    import calendar

    first_day = specified_day
    days_of_month = calendar.monthrange(specified_day.year, specified_day.month)[1]
    last_day = specified_day + timedelta(days=days_of_month - 1)

    s2i = {
        'date_ymd': 0,
        'stu': 1,
        'spo': 2,
        'rd': 3,
        'joy': 4,
        'mus': 5,
        'was': 6,
        'stu_pct': 7,
        'spo_pct': 8,
        'rd_pct': 9,
        'joy_pct': 10,
        'mus_pct': 11,
        'was_pct': 12,
        'total_hours': 13,
    }

    i2s = ['' for i in range(0, 14)]
    for s in s2i:
        i2s[s2i[s]] = s

    import os
    os.system('mysql.server start')

    import pymysql
    conn = pymysql.connect(host='127.0.0.1', user='test', password='88887777', database='life_log')
    cursor = conn.cursor()

    while first_day < datetime(2015, 10, 1):

        ##############################
        # get Day Logs of the Month
        ##############################
        sql = r'select ' + ', '.join(i2s) + ' from day_log where ' \
              + 'date_ymd >= "' + first_day.strftime('%Y-%m-%d') + '" and ' \
              + 'date_ymd <= "' + last_day.strftime('%Y-%m-%d') + '"'
        print('\n', sql, '\n')

        cursor.execute(sql)
        days = cursor.fetchall()

        if days_of_month != len(days):
            print('Just %d days data, not enough!' % len(days))
            cursor.close()
            conn.close()
            exit(1)

        ##############################
        # make Month Stat
        ##############################
        types = {}
        for i in range(1, 7):
            types[i2s[i]] = {'hours': 0, 'pct': 0}

        for d in days:
            print(d[s2i['date_ymd']],
                  'stu', d[s2i['stu']], d[s2i['stu_pct']],
                  'spo', d[s2i['spo']], d[s2i['spo_pct']],
                  'rd', d[s2i['rd']], d[s2i['rd_pct']],
                  'joy', d[s2i['joy']], d[s2i['joy_pct']],
                  'mus', d[s2i['mus']], d[s2i['mus_pct']],
                  'was', d[s2i['was']], d[s2i['was_pct']],
                  'all', d[s2i['total_hours']])
            for i in range(1, 7):
                types[i2s[i]]['hours'] += d[i]
        print()

        all_hours = 0
        for i in range(1, 7):
            all_hours += types[i2s[i]]['hours']

        for i in range(1, 7):
            types[i2s[i]]['pct'] = round(types[i2s[i]]['hours'] / all_hours * 1000) / 10
            print(i2s[i], types[i2s[i]]['hours'], 'h', types[i2s[i]]['pct'], '%')

        print('total_hours:', all_hours)

        ##############################
        # save Month Stat to DB
        ##############################
        sql = r'insert into month_log(month_1st, days, stu, stu_pct, spo, spo_pct, rd, rd_pct, joy, joy_pct, mus, mus_pct, was, was_pct, total_hours, created_time) values("' \
              + first_day.strftime('%Y/%m/%d') + '", "' + str(days_of_month) + '"'

        for i in range(1, 7):
            sql += ', ' + str(types[i2s[i]]['hours'])
            sql += ', ' + str(types[i2s[i]]['pct'])
        sql += ', ' + str(all_hours) + ', "' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '")'
        print(sql)

        cursor.execute(sql)

        ##############################
        # prepare Vars
        ##############################
        first_day = first_day + timedelta(days=days_of_month)
        days_of_month = calendar.monthrange(first_day.year, first_day.month)[1]
        last_day = first_day + timedelta(days=days_of_month - 1)

    cursor.close()
    conn.commit()
    conn.close()
