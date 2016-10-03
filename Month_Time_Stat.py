#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    from datetime import datetime, timedelta
    today = datetime.now()

    import sys
    if len(sys.argv) > 1:
        today = datetime.strptime(
            sys.argv[1],
            '%m/%d/%y'
        )
        print('Today =', today)

    # {datetime}.weekday() == 0 表示 周一
    if 1 != today.day:
        print('It isn\'t 1st day of the new month today!')
        exit(1)

    last_day = today - timedelta(days=1)
    first_day = today - timedelta(days=last_day.day)
    days_of_month = last_day.day

    s2i = {
        'date_ymd':     0,
        'stu':          1,
        'spo':          2,
        'rd':           3,
        'joy':          4,
        'mus':          5,
        'was':          6,
        'stu_pct':      7,
        'spo_pct':      8,
        'rd_pct':       9,
        'joy_pct':      10,
        'mus_pct':      11,
        'was_pct':      12,
        'total_hours':  13,
    }

    i2s = ['' for i in range(0, 14)]
    for s in s2i:
        i2s[s2i[s]] = s

    ##############################
    # Has made the Month Stat?
    ##############################
    import os
    os.system('mysql.server start')

    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        user='test',
        password='88887777',
        database='life_log'
    )
    cursor = conn.cursor()

    sql = r'select * from month_log where month_1st = "%s"' \
          % first_day.strftime('%Y/%m/%d')

    cursor.execute(sql)
    month_log = cursor.fetchall()
    print(month_log)

    if 0 != len(month_log):
        print('The stat of this month has existed!')
        cursor.close()
        conn.close()
        exit(1)

    ##############################
    # get Day Logs of the Month
    ##############################
    sql = r'select %s from day_log where date_ymd >= "%s" and date_ymd <= "%s"' % (
        ', '.join(i2s),
        first_day.strftime('%Y-%m-%d'),
        last_day.strftime('%Y-%m-%d')
    )

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
        print(
            d[s2i['date_ymd']],
            'stu', d[s2i['stu']], d[s2i['stu_pct']],
            'spo', d[s2i['spo']], d[s2i['spo_pct']],
            'rd', d[s2i['rd']], d[s2i['rd_pct']],
            'joy', d[s2i['joy']], d[s2i['joy_pct']],
            'mus', d[s2i['mus']], d[s2i['mus_pct']],
            'was', d[s2i['was']], d[s2i['was_pct']],
            'all', d[s2i['total_hours']]
        )

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
    # export Note & get content
    ##############################
    note_name = first_day.strftime('%Y/%m stu spo was')

    import random
    enex_path = '/Users/IceHe/Documents/Enex/statistics/%s_Month_Log_ori_%s_%s.enex' % (
        first_day.strftime('%Y-%m'),
        datetime.now().strftime('%H%M%S'),
        str(random.randint(100, 999))
    )

    print('enex_path:', enex_path)

    print('Export Note:')
    os.system('osascript /Users/IceHe/Documents/AppleScript/Evernote/note_export_enex.scpt "%s" "%s"' % (
        note_name,
        enex_path
    ))

    import codecs
    with codecs.open(enex_path, 'r', 'utf-8') as f:
        content = f.read()

    month_1st = datetime(first_day.year, first_day.month, 1)

    import re
    ori_month_stat = re.findall(
        r'(<div>Monthly<\/div>[\s\S]*?\n<div>总<\/div>)',
        content,
        re.S
    )[0]

    ##############################
    # output Month Stat
    ##############################
    types_str = ' 学动读乐必废'
    type_ary = [c for c in types_str]

    mod_str = ori_month_stat
    for i in range(1, 7):
        mod_str = re.sub(
            r'(%s([^<]*)?)' % type_ary[i],
            '%s%s，%s' % (
                type_ary[i],
                types[i2s[i]]['hours'],
                types[i2s[i]]['pct']
            ),
            mod_str
        )

    mod_str = re.sub(
        r'(<div>/</div>)',
        '<div>%s</div>' % first_day.strftime('%Y/%m'),
        mod_str
    )
    mod_str = re.sub(r'(总([^<]*)?)', '%s%s' % ('总', all_hours), mod_str)

    content = content.replace(ori_month_stat, mod_str)
    content = re.sub(
        r'(<title>%s stu spo was</title>)' % first_day.strftime('%Y/%m'),
        '<title>%s stu%s spo%s was%s</title>' % (
            first_day.strftime('%Y/%m'),
            round(types[i2s[1]]['pct']),
            round(types[i2s[2]]['pct']),
            round(types[i2s[6]]['pct'])
        ),
        content
    )

    ##############################
    # save Month Stat to DB
    ##############################
    sql = r'insert into month_log(month_1st, days, ' \
          r'stu, stu_pct, spo, spo_pct, rd, rd_pct, ' \
          r'joy, joy_pct, mus, mus_pct, was, was_pct, ' \
          r'total_hours, created_time) values("%s", "%s"' % (
              first_day.strftime('%Y/%m/%d'),
              str(days_of_month)
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

    ##############################
    # import Note
    ##############################
    enex_import_path = enex_path.replace('_ori_', '_edt_')

    with codecs.open(enex_import_path, 'w', 'utf-8') as f:
        f.write(content)

    print(note_name)
    print('Delete Note:')
    # 删除笔记操作，请注意！
    os.system(
        'osascript /Users/IceHe/Documents/AppleScript/Evernote/note_delete_no_confirm.scpt "%s"'
        % note_name
    )

    print('Import Note:')
    os.system(
        'osascript /Users/IceHe/Documents/AppleScript/Evernote/note_import.scpt "%s" "%s"' % (
            enex_import_path,
            first_day.strftime('%Y/%m')
        )
    )
