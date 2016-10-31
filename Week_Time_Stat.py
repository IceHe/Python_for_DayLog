#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    from datetime import datetime, timedelta
    today = datetime.now()

    import sys
    if len(sys.argv) > 1:
        today = datetime.strptime(sys.argv[1], '%m/%d/%y')

    # {datetime}.weekday() == 0 表示 周一
    if 0 != today.weekday():
        print('It isn\'t Monday today!')
        exit(1)

    monday = today - timedelta(days=7)
    sunday = today - timedelta(days=1)

    print('Today =', today)
    print('Monday =', monday)
    print('Sunday =', sunday)

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
    # Has made the Week Stat?
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

    sql = r'select * from week_log where from_date = "%s"' \
          % monday.strftime('%Y/%m/%d')

    cursor.execute(sql)
    week_log = cursor.fetchall()
    if 0 != len(week_log):
        print('The stat of this week has existed!')
        cursor.close()
        conn.close()
        exit(1)

    ##############################
    # get Day Logs of the Week
    ##############################
    sql = r'select %s from day_log where date_ymd >= "%s" and date_ymd <= "%s"' % (
        ', '.join(i2s),
        monday.strftime('%Y-%m-%d'),
        sunday.strftime('%Y-%m-%d')
    )
    print('\n', sql, '\n')

    cursor.execute(sql)
    days = cursor.fetchall()

    if 7 != len(days):
        print('Just %d days data, not enough!' % len(days))
        cursor.close()
        conn.close()
        exit(1)

    ##############################
    # make Week Stat
    ##############################
    types = {}
    for i in range(1, 7):
        types[i2s[i]] = {
            'hours': 0,
            'pct': 0
        }

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
    month_log_at = monday
    if month_log_at.month < (month_log_at + timedelta(days=3)).month:
        month_log_at = month_log_at + timedelta(days=3)
    print(month_log_at)

    note_name = month_log_at.strftime('%Y/%m ')

    import random
    enex_path = '/Users/IceHe/Documents/Enex/statistics/%s_Week_Log_ori_%s_%s.enex' % (
        month_log_at.strftime('%Y-%m'),
        datetime.now().strftime('%H%M%S'),
        str(random.randint(100, 999))
    )

    print('enex_path:', enex_path)

    print('Export Note:')
    cmd = 'osascript /Users/IceHe/Documents/AppleScript/Evernote/note_export_enex_with_nbname.scpt "%s stu" "%s" "%s"' % (
        note_name,
        month_log_at.strftime('%Y/%m'),
        enex_path
    )

    print(cmd)
    os.system(cmd)

    import codecs
    with codecs.open(enex_path, 'r', 'utf-8') as f:
        content = f.read()

    month_1st = datetime(month_log_at.year, month_log_at.month, 1)

    # 在周三之后
    if month_1st.weekday() > 3:
        month_1st_week_monday = month_1st + timedelta(days=7 - month_1st.weekday())
    # 周四之前
    else:
        month_1st_week_monday = month_1st - timedelta(days=month_1st.weekday())

    week_num = (monday - month_1st_week_monday).days // 7 + 1
    print("week_num:", week_num)

    import re
    ori_week_stat = re.findall(
        r'(<div>Week %s</div>[\s\S]*?<div><br/></div>)' % (
            str(week_num),
        ),
        content,
        re.S
    )[0]

    ##############################
    # output Week Stat
    ##############################
    types_str = ' 学动读乐必废'
    type_ary = [c for c in types_str]

    mod_str = ori_week_stat
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
        r'(<div>// ~ //<\/div>)',
        '<div>%s ~ %s</div>' % (
            monday.strftime('%y/%m/%d'),
            sunday.strftime('%y/%m/%d')
        ),
        mod_str
    )

    mod_str = re.sub(
        r'(总([^<]*)?)',
        '%s%s' % ('总', all_hours),
        mod_str
    )

    content = content.replace(ori_week_stat, mod_str)

    ##############################
    # save Week Stat to DB
    ##############################
    sql = r'insert into week_log(from_date, to_date, ' \
          r'stu, stu_pct, spo, spo_pct, rd, rd_pct, ' \
          r'joy, joy_pct, mus, mus_pct, was, was_pct, ' \
          r'total_hours, created_time) values("%s", "%s"' % (
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

    ##############################
    # import Note
    ##############################
    enex_import_path = enex_path.replace('_ori_', '_edt_')

    with codecs.open(enex_import_path, 'w', 'utf-8') as f:
        f.write(content)

    print(note_name)
    print('Delete Note:')
    # 删除笔记操作，请注意！
    os.system('osascript /Users/IceHe/Documents/AppleScript/Evernote/note_delete_with_nbname_no_confirm.scpt "%s stu" "%s"' % (
        note_name,
        month_log_at.strftime('%Y/%m')
    ))

    print('Import Note:')
    os.system('osascript /Users/IceHe/Documents/AppleScript/Evernote/note_import.scpt "%s" "%s"' % (
        enex_import_path,
        month_log_at.strftime('%Y/%m')
    ))
