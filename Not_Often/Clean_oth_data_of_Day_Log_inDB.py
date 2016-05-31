#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

########################
# TODO: NOT Completed! #
########################

if __name__ == '__main__':

    # import re
    # ary = ['开好头（上午全力工作）', '朋友圈（临睡）1234', '微博（琐碎时间）12']
    # for x in ary:
    #     if re.match(r'.*?\d+$', x):
    #         print(x)
    # exit(0)

    from datetime import datetime
    date_1st = datetime(2015, 10, 1)
    date_last = datetime(2015, 11, 30)

    ##############################
    # init DB conn
    ##############################
    import os
    os.system('mysql.server start')

    import pymysql
    conn = pymysql.connect(user='test', password='88887777', database='life_log')
    cursor = conn.cursor()

    sql = r'select date_ymd, oth_data from day_log where date_ymd >= "' \
          + date_1st.strftime('%y-%m-%d') \
          + r'" and date_ymd <= "' \
          + date_last.strftime('%y-%m-%d') + r'"'

    cursor.execute(sql)
    day_logs = cursor.fetchall()

    import json
    import re
    for day_log in day_logs:

        result = ''
        is_deal = False

        print(day_log[0])
        # del(day_log[1]['discipline'])
        print(json.loads(day_log[1])['discipline'])
        for item in json.loads(day_log[1])['discipline']:
            if re.match(r'.*?\d+$', [k for k in item][0]):
                print([k for k in item][0])
                print(re.sub(r'\d+$', '', [k for k in item][0]))
                result = day_log[1].replace([k for k in item][0], re.sub(r'\d+$', '', [k for k in item][0]))
                is_deal = True
                # print(re.sub(r'\d+$', '', [k for k in item][0]))
                # print(m[0])
                # for x in m.groups():
                #     print(x)
            # print()
        if is_deal:
            print(json.loads(result)['discipline'], '\n')
        continue

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

