#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days = 1))
    # yesterday = datetime(2015, 11, 17)
    yesterday_str = yesterday.strftime('%y/%m/%d')

    note_name = yesterday_str + ' stu spo'
    # note_name = yesterday_str

    import random
    enex_path = '/Users/IceHe/Coding/Enex/statistics/' + yesterday_str.replace('/', '-')\
                + '_Day_Log_ori_' + datetime.now().strftime('%H%M%S')\
                + '_' + str(random.randint(100, 999)) + '.enex'

    print('enex_path:', enex_path)


    ##############################
    # Has made the Week Stat?
    ##############################
    import os
    os.system('mysql.server start')

    import mysql.connector
    conn = mysql.connector.connect(user = 'test', password = '88887777', database='life_log')
    cursor = conn.cursor()

    sql = r'select * from day_log where date_ymd = "' + yesterday.strftime('%y-%m-%d') + '"'
    cursor.execute(sql)
    week_log = cursor.fetchall()
    if 0 != len(week_log):
        print('The stat of yesterday has existed!')
        cursor.close()
        conn.close()
        exit(1)


    ##############################
    # export Note & get content
    ##############################
    import os
    print('Export Note:')
    os.system('osascript /Users/IceHe/Coding/AppleScript/Evernote/note_export_enex.scpt "'
              + note_name + '" "' + enex_path + '"')

    import codecs
    with codecs.open(enex_path, 'r', 'utf-8') as f:
        content = f.read()


    ##############################
    # get Time Detail
    ##############################
    import re
    matches = re.findall(r'(?:<div><b>)(# Time Detail[\s\S]*?(?:\d\d\d\d睡<\/div>\n<div><br\/><\/div>))?', content, re.S)
    # matches = re.findall(r'(<div><b># Time Detail[\s\S]*?(?:\d\d\d\d睡<\/div>\n<div><br\/><\/div>))?', content, re.S)
    print(matches)
    time_detail = [m for m in matches if m != ''][0]

    type_str = '学动读乐必废'
    time_slots = re.findall(r'(\d\d\d\d)([' + type_str + '])', time_detail)

    print('time_slots:', time_slots)


    ##############################
    # stat Time Detail
    ##############################
    def format_time(t):
        # 如730便于表示七点半，但不便于计算小时数，所以将其中的30凑成50！
        if 30 == t % 100:
            return t + 20
        elif 0 != t % 100:
            print('Time Point Format Error! ')
            exit(1)
        return t

    time_got_up = format_time(int(re.findall(r'(\d\d\d\d)起', time_detail)[0]))

    timeline = []
    for t in time_slots:
        to_time = format_time(int(t[0]))
        # 极少在4:00后入睡，入睡前的时间都统计到前一天去，加2400方便时间计算
        if to_time <= 400:
            to_time += 2400
        timeline.append({'to_time': to_time, 'type': t[1]})

    def format_digit(digit):
        if 0 == digit * 10 % 10:
            return int(digit) # integer
        return digit # float %.1f

    from_time = time_got_up
    stat_str = ''
    for t in timeline:
        t['hours'] = format_digit((t['to_time'] - from_time) / 100)
        stat_str += ''.join([t['type'] for i in range(int(t['hours'] * 2))])
        from_time = t['to_time']

    print('timeline:', timeline)


    ##############################
    # update Time Detail
    ##############################
    # \xa0是空格，因为导入Evernote中时是以html导入的，多个空格会当作一个空格处理
    matches = re.findall(r'(?:>)((\d\d\d\d[' + type_str + '] .*?)(?:[ \xa0])?([\d\.]*?)?(?:<\/))', time_detail)

    def format_hours(hours):
        if 0.5 == hours:
            return '.5'
        return str(hours)

    time_detail_edt = time_detail
    i = 0
    for m in matches:
        if '' == m[2]:
            time_detail_edt = time_detail_edt.replace(m[0], m[1] + ' ' + format_hours(timeline[i]['hours']) + '</')
        i += 1

    content = content.replace(time_detail, time_detail_edt)

    # 根据睡前最后一项活动的结束时间，来更正睡眠开始时间！
    content = re.sub('\d\d\d\d睡<\/div>\n', str(time_slots[-1][0]) + '睡</div>\n', content)


    ##############################
    # stat Time Table
    ##############################
    # 0700 / 50 = 14
    # 7点开始算时间，每半小时一个时段，7点前一共有14个时段
    # 14 - 3 * 2 = 8
    # 一天的开始我几乎不从3点开始（起床），也几乎不从3点结束（睡觉）
    # 所以一天最早从3点算起，7点的前一个时段算是一天的第8个时段

    # 半小时为一个时段，一天48个时段
    time_ary = ['' for i in range(48)]
    slot_num = time_got_up // 50 - 6
    for type in [c for c in stat_str]:
        time_ary[slot_num] = type
        slot_num += 1

    # 一天24小时，即一天24个双时段
    start_hour = time_got_up // 100 - 3
    end_hour = (timeline[len(timeline) - 1]['to_time'] - 50) // 100 - 3

    hour_ary = ['〇〇，' for i in range(24)]
    for i in range(start_hour, end_hour + 1):
        if '' == time_ary[i * 2]:
            hour_ary[i] = '〇' + time_ary[i * 2 + 1] + '，'
        elif '' == time_ary[i * 2 + 1]:
            hour_ary[i] = time_ary[i * 2] + '。'
            for k in range(i + 1, 24):
                hour_ary[k] = ''
        elif i == end_hour:
            hour_ary[i] = time_ary[i * 2] + time_ary[i * 2 + 1] + '。'
            for k in range(i + 1, 24):
                hour_ary[k] = ''
        else:
            hour_ary[i] = time_ary[i * 2] + time_ary[i * 2 + 1] + '，'

    def format_hh(hour):
        if 0 <= hour and hour < 10:
            return '0' + str(hour)
        return str(hour)


    ##############################
    # make Time Table
    ##############################
    time_table = '# Time Table</b></div>\n'

    for i in range(start_hour // 4, end_hour // 4 + 1):
        time_table += '<div>' + format_hh(i * 4 + 3)\
                      + '-' + format_hh((i * 4 + 6) % 24)\
                      + ' ' + ''.join(hour_ary[(i * 4):(i * 4 + 4)])\
                      + '</div>\n'

    time_table += '<div><br/></div>'

    print('\n', time_table)


    ##############################
    # output Time Table
    ##############################
    matches = re.findall(r'(?:<div><b>)(# Time Table[\s\S]*?(?:<div><br\/><\/div>))?', content, re.S)
    target_str = [m for m in matches if m != ''][0]
    content = content.replace(target_str, time_table)


    ##############################
    # make Time Stat
    ##############################
    def format_digit(digit):
        if 0 == digit * 10 % 10:
            return int(digit)
        return digit

    all_hours = format_digit(len(stat_str) / 2)
    type_ary = [ch for ch in type_str]
    type_stat = {}

    print('\n# Time Stat')

    for type in type_ary:
        type_stat[type] = {'hours': format_digit(stat_str.count(type) / 2)}
        type_stat[type]['pct'] = format_digit(round(type_stat[type]['hours'] / all_hours * 1000) / 10) # 只精确到十分位
        print('%s%s，%s' % (type, type_stat[type]['hours'], type_stat[type]['pct']))

    print('时', all_hours)


    ##############################
    # output Time Stat
    ##############################
    matches = re.findall(r'(<div><b># Time Stat<\/b><\/div>[\s\S]*(?:<div><br\/><\/div>))?', content, re.S)
    target_str = [s for s in matches if s != ''][0]

    mod_str = target_str
    for type in type_ary:
        mod_str = re.sub(r'(' + type + r'([^<]*)?)', '%s%s，%s' % (type, type_stat[type]['hours'], type_stat[type]['pct']), mod_str)
    mod_str = re.sub(r'(总([^<]*)?)', '%s%s' % ('总', all_hours), mod_str)

    content = content.replace(target_str, mod_str)


    ##############################
    # save Time Stat in DB
    ##############################
    sql = r'insert into day_log(date_ymd, stu, stu_pct, spo, spo_pct, rd, rd_pct, joy, joy_pct, mus, mus_pct, was, was_pct, total_hours, created_time) values("' \
          + yesterday.strftime('%Y/%m/%d') + '"'
    for type in type_ary:
        sql += ', ' + str(type_stat[type]['hours'])
        sql += ', ' + str(type_stat[type]['pct'])
    sql += ', ' + str(all_hours) + ', "' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '")'

    cursor.execute(sql)


    ##############################
    # update Note Name
    ##############################
    note_name_str = re.findall(r'(<title>.*?<\/title>)', content, re.S)[0]

    new_note_name = '<title>' + yesterday_str\
                    + ' stu' + str(round(type_stat['学']['pct']))\
                    + ' spo' + str(round(type_stat['动']['pct']))
    if 0 != type_stat['废']['pct']:
        new_note_name += ' was' + str(round(type_stat['废']['pct']))
    new_note_name += '</title>'

    content = content.replace(note_name_str, new_note_name)


    ##############################
    # stat Discipline
    ##############################
    import re
    matches = re.findall(r'(?:<div><b>)(# Discipline[\s\S]*?)(?:<div><b>#)', content, re.S)
    discipline_detail = [m for m in matches if m != ''][0]

    discipline_list = re.findall(r'(?:<div>)(<en-todo([^/]*)?\/>([^<]*))(?:<\/div>)', discipline_detail)

    discipline_stat = []
    for x in discipline_list:
        discipline_stat.append({x[2].replace(r'\xa0', ' '): ('' == x[1])})


    ##############################
    # save Discipline Result in DB
    ##############################
    import json
    discipline_json = json.dumps({'discipline': discipline_stat})

    sql = r'update day_log set oth_data = "' \
          + discipline_json.replace('\\', '\\\\').replace('"', r'\"') \
          + '" where date_ymd = "' + yesterday.strftime('%Y-%m-%d') + '"'
    print(sql)

    cursor.execute(sql)

    cursor.close()
    conn.commit()
    conn.close()

    # exit(0)


    ##############################
    # import Note
    ##############################
    enex_import_path = enex_path.replace('_ori_', '_edt_')

    with codecs.open(enex_import_path, 'w', 'utf-8') as f:
        f.write(content)

    print(note_name)
    print('Delete Note:')
    # 高危操作，请注意！
    os.system('osascript /Users/IceHe/Coding/AppleScript/Evernote/note_delete_no_confirm.scpt "' + note_name + '"')
    # os.system('osascript /Users/IceHe/Coding/AppleScript/Evernote/note_delete.scpt "'
    #           + note_name + '"')

    print('Import Note:')
    os.system('osascript /Users/IceHe/Coding/AppleScript/Evernote/note_import.scpt "'
              + enex_import_path + '" "' + yesterday.strftime('%Y/%m') + '"')
