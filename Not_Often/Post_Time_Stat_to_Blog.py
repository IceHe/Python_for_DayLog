#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

from datetime import datetime, timedelta
import calendar

def post_time_stat_to_blog(day):

    cur_month_1st = datetime(day.year, day.month, 1)

    notebook_name = cur_month_1st.strftime('%Y/%m')
    note_name = cur_month_1st.strftime('%Y/%m')

    ##############################
    # export Note
    ##############################
    import os
    print('Export Note:')
    html_export_path = '/Users/IceHe/Documents/Enex/lifelog_month_stat/' + note_name.replace('/', '-')
    cmd = 'osascript /Users/IceHe/Documents/AppleScript/Evernote/note_export_html_with_nbname.scpt "' \
          + note_name + '" "' + notebook_name + '" "' + html_export_path + '"'
    os.system(cmd)
    print(cmd)
    print(html_export_path)

    ##############################
    # get Content
    ##############################
    html_file_name = os.listdir(html_export_path)[0]
    if not note_name.replace('/', '_') in html_file_name:
        print('Cannot find the specific html file!')
        exit(1)
    print(html_file_name)

    import codecs
    with codecs.open(html_export_path + '/' + html_file_name, 'r', 'utf-8') as f:
        content = f.read()

    import re
    note_title = re.findall(r'(?:<title>)([\s\S]*?)(?:<\/title>)', content, re.S)[0]
    output = re.findall(r'(?:<body[^>]*?>)([\s\S]*?)(?:<\/body>)', content, re.S)[0]

    ##############################
    # process Text Content
    ##############################
    cur_month_last_day = cur_month_1st + timedelta(days=calendar.monthrange(day.year, day.month)[1] - 1)

    c_Ym = day.strftime('%Y/%m')

    output = 'title: ' + note_title + '\n' \
             + 'date: ' + cur_month_last_day.strftime('%Y-%m-%d %H:%M:%S') + '\n' \
             + 'toc: false\n' \
             + '---\n' \
             + '[返回月历 **Back to Month ^**](/lifelogs/' \
             + c_Ym + '/index.html)\n<br/>' \
             + output.replace('\n', '')

    ##############################
    # output Post
    ##############################
    lifelog_dir = '/Users/IceHe/Documents/Blog/icehe.me/source/lifelogs'
    cur_year_dir = lifelog_dir + '/' + day.strftime('%Y')
    cur_month_dir = cur_year_dir + '/' + day.strftime('%m')
    time_stat_path = '%s/time_stat.md' % cur_month_dir

    with codecs.open(time_stat_path, 'w', 'utf-8') as f:
        f.write(output)

    ##############################
    # add link to Month Log page
    ##############################
    month_log_path = '%s/index.md' % cur_month_dir
    with codecs.open(month_log_path, 'a', 'utf-8') as f:
        f.write('32. [**Summary %s**](/lifelogs/%s/%s/time_stat.html)\n' % (note_title, day.year, day.strftime('%m')))

    ##############################
    # add Time Stat Brief to Month Log Title
    ##############################
    with codecs.open(month_log_path, 'r', 'utf-8') as f:
        month_log = f.read()

    month_index_title = re.findall(r'((title: \d\d\d\d\/\d\d)([^\n]*))', month_log, re.S)[0]
    print(month_index_title)

    import pymysql
    conn = pymysql.connect(user='test', password='88887777', database='life_log')
    cursor = conn.cursor()

    sql = 'select stu_pct, spo_pct, was_pct from month_log where month_1st = "%s"' % day.strftime('%Y/%m/%d')
    cursor.execute(sql)

    month_time_stat = cursor.fetchall()
    month_time_stat = [round(x) for x in month_time_stat[0]]

    new_month_index_title = '%s stu%s spo%s was%s' % (month_index_title[1], month_time_stat[0], month_time_stat[1], month_time_stat[2])

    cursor.close()
    conn.close()

    month_log = month_log.replace(month_index_title[0], new_month_index_title)
    with codecs.open(month_log_path, 'w', 'utf-8') as f:
         f.write(month_log)


if __name__ == '__main__':

    # Single

    today = datetime.now()
    last_month_last_day = datetime(today.year, today.month, 1) - timedelta(days=1)
    last_month_1st = last_month_last_day - timedelta(days=calendar.monthrange(last_month_last_day.year, last_month_last_day.month)[1] - 1)

    print(last_month_1st)
    post_time_stat_to_blog(last_month_1st)

    exit(0)

    # Batch

    day = datetime(2015, 12, 1)
    if 1 != day.day:
        print('Error: day must be 1st of the month!')
        exit(1)

    while day < datetime(2016, 1, 1):
        post_time_stat_to_blog(day)
        day += timedelta(days=calendar.monthrange(day.year, day.month)[1])
