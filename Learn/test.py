#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    import json
    json_str = '{"discipline": [{"key": "\u65e9\u8d77 (0830\u524d)", "value": false}, {"key": "\u65e9\u9910", "value": false}, {"key": "\u82f1\u8bed", "value": false}, {"key": "\u8fd0\u52a8", "value": false}, {"key": "\u5f00\u597d\u5934\uff08\u4e0a\u5348\u5168\u529b\u5de5\u4f5c\uff09", "value": false}, {"key": "\u670b\u53cb\u5708\u00a0(\u508d\u665a/\u4e34\u7761)1", "value": false}, {"key": "\u5fae\u535a (\u4e34\u7761)", "value": false}, {"key": "\u53cd\u7701", "value": false}, {"key": "\u4e0d\u634b/\u62c9\u5934\u53d1", "value": true}, {"key": "\u53ea\u559d\u6e29\u767d\u5f00", "value": false}, {"key": "\u65e9\u7761 (2330\u524d)", "value": false}]}'
    # json_str = '{"[\u00a0]": false}'

    print(json.loads(json_str))

    exit(0)

    from datetime import datetime, timedelta
    today = datetime(2015, 11, 30)
    # today = datetime(2015, 11, 16)
    # today = datetime(2015, 9, 28)
    # today = datetime(2015, 8, 31)
    # today = datetime(2015, 7, 27)

    # {datetime}.weekday() == 0 表示 周一
    if 0 != today.weekday():
        print('It isn\'t Monday today!')
        exit(1)

    monday = today
    sunday = today + timedelta(days = 6)
    print('monday', monday)
    print('sunday', sunday)

    month_log_at = monday
    print('monday=', monday.weekday())
    if month_log_at.month < (month_log_at + timedelta(days = 3)).month:
        month_log_at = month_log_at + timedelta(days = 3)
    print(month_log_at)

    month_1st = datetime(month_log_at.year, month_log_at.month, 1)
    if month_1st.weekday() > 3:
        month_1st_week_monday = month_1st + timedelta(days = 7 - month_1st.weekday())
    else:
        month_1st_week_monday = month_1st - timedelta(days = month_1st.weekday())

    week_num = (monday - month_1st_week_monday).days // 7 + 1
    print("week_num:", week_num)

    ##############################
    # MySQL
    ##############################
    # import pymysql
    #
    #
    # conn = pymysql.connect(user = 'test', password = '88887777', database='life_log')
    # cursor = conn.cursor()
    #
    # cursor.execute(r'select * from day_log')
    # print(cursor.rowcount)
    #
    # values = cursor.fetchall()
    # print(values)
    # print(values[0])
    # print(values[0][1].year)
    #
    # cursor.execute(r'insert into day_log(date_ymd, stu, spo, rd, joy, mus, was) values("2015-10-21", 1.0, 2, 3, 4.0, 0, 6.5)')
    #
    # cursor.close()
    # conn.commit()
    # conn.close()
