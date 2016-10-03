#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    from datetime import datetime, timedelta
    from_date = datetime(2014, 12, 29)

    # {datetime}.weekday() == 0 表示 周一
    if 0 != from_date.weekday():
        print('The from_date isn\'t Monday!')
        exit(1)

    while from_date <= datetime(2015, 10, 12):
        from_date = from_date + timedelta(days=7)

        monday = from_date
        sunday = from_date + timedelta(days=6)

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

        ##############################
        # get Day Logs from the Week
        ##############################
        import pymysql
        conn = pymysql.connect(host='127.0.0.1', user='test', password='88887777', database='life_log')
        cursor = conn.cursor()

        sql = r'select ' + ', '.join(i2s) + ' from day_log where ' \
              + 'date_ymd >= "' + monday.strftime('%Y-%m-%d') + '" and ' \
              + 'date_ymd <= "' + sunday.strftime('%Y-%m-%d') + '"'
        print('\n', sql, '\n')

        cursor.execute(sql)
        days = cursor.fetchall()

        ##############################
        # make Week Stat
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

        if 7 != len(days):
            print('Error: Get %d days data!' % len(days))
            exit(1)

        all_hours = 0
        for i in range(1, 7):
            all_hours += types[i2s[i]]['hours']

        for i in range(1, 7):
            types[i2s[i]]['pct'] = round(types[i2s[i]]['hours'] / all_hours * 1000) / 10
            print(i2s[i], types[i2s[i]]['hours'], 'h', types[i2s[i]]['pct'], '%')

        print('total_hours:', all_hours)

        ##############################
        # save Week Stat to DB
        ##############################
        sql = r'insert into week_log(from_date, to_date, ' \
              r'stu, stu_pct, spo, spo_pct, rd, rd_pct, joy, joy_pct, mus, mus_pct, was, was_pct, ' \
              r'total_hours, created_time) values("%s", "%s")' % (
                  monday.strftime('%Y/%m/%d'),
                  sunday.strftime('%Y/%m/%d')
              )

        for i in range(1, 7):
            sql += ', %s, %s' % (
                str(types[i2s[i]]['hours']),
                str(types[i2s[i]]['pct'])
            )

        sql += ', %s, "%s")' % (
            str(all_hours),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        print(sql)

        cursor.execute(sql)

        cursor.close()
        conn.commit()
        conn.close()
