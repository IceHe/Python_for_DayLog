#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    ################
    exit(0)  # Switch
    ################

    from datetime import datetime, timedelta

    date_1st = datetime(2014, 12, 29)
    days = 3

    for i in range(0, days):
        date = date_1st + timedelta(days=i)

        date_str = date.strftime('%y/%m/%d')

        note_name = date_str
        print(note_name)

        import random
        enex_path = '/Users/IceHe/Documents/Enex/stat_to_db/' + date_str.replace('/', '-')\
                    + '_Day_Log_ori_' + datetime.now().strftime('%H%M%S')\
                    + '_' + str(random.randint(100, 999)) + '.enex'

        print('enex_path:', enex_path)

        ##############################
        # export Note & get content
        ##############################
        import os

        print('Export Note:')
        os.system('osascript /Users/IceHe/Documents/AppleScript/Evernote/note_export_enex.scpt "'
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
                return int(digit)  # integer
            return digit  # float %.1f

        from_time = time_got_up
        stat_str = ''
        for t in timeline:
            t['hours'] = format_digit((t['to_time'] - from_time) / 100)
            stat_str += ''.join([t['type'] for i in range(int(t['hours'] * 2))])
            from_time = t['to_time']

        print('timeline:', timeline)

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
        # save Time Stat in Database
        ##############################
        import pymysql
        conn = pymysql.connect(host='127.0.0.1', user='test', password='88887777', database='life_log')
        cursor = conn.cursor()

        sql = r'insert into day_log(date_ymd, stu, stu_pct, spo, spo_pct, rd, rd_pct, joy, joy_pct, mus, mus_pct, was, was_pct, total_all_hours, created_time) values("'\
              + date.strftime('%Y/%m/%d') + '"'
        for type in type_ary:
            sql += ', ' + str(type_stat[type]['hours'])
            sql += ', ' + str(type_stat[type]['pct'])

        sql += ', ' + str(all_hours) + ', "' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '")'

        cursor.execute(sql)

        cursor.close()
        conn.commit()
        conn.close()
