#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    from datetime import datetime, timedelta
    date_1st = datetime(2015, 10, 1)
    days = 31 + 17

    ##############################
    # init DB conn
    ##############################
    import os
    os.system('mysql.server start')

    import pymysql
    conn = pymysql.connect(host='127.0.0.1', user='test', password='88887777', database='life_log')
    cursor = conn.cursor()

    for i in range(0, days):
        date = date_1st + timedelta(days=i)
        date_str = date.strftime('%y/%m/%d')
        note_name = date_str

        import random
        enex_path = '/Users/IceHe/Documents/Enex/tmp/' + date_str.replace('/', '-')\
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
        print(discipline_json)

        sql = r'update day_log set oth_data = "' \
              + discipline_json.replace('\\', '\\\\').replace('"', r'\"') \
              + '" where date_ymd = "' + date.strftime('%Y-%m-%d') + '"'
        print(sql)

        cursor.execute(sql)

    cursor.close()
    conn.commit()
    conn.close()
