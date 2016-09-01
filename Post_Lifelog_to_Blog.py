#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import calendar

__author__ = 'IceHe'


def post_monthlog_to_blog(day, lifelog_dir):

    prev_month_last_day = day - timedelta(days=day.day)
    prev_month = prev_month_last_day - timedelta(
        days=prev_month_last_day.day - 1
    )
    next_month = day + timedelta(
        days=calendar.monthrange(day.year, day.month)[1] - day.day + 1
    )

    content = 'title: ' + day.strftime('%Y/%m') + '\n' \
              + 'date: ' + next_month.strftime('%Y-%m-01 00:00:00') + '\n' \
              + 'toc: false\n' \
              + '---\n' \
              + '[**< ' + prev_month.strftime('%b. %Y') \
              + '** - Prev 上一月](/lifelogs/' \
              + prev_month.strftime('%Y/%m') \
              + '/index.html) &nbsp; &nbsp; | &nbsp; &nbsp; [下一月 Next - **' \
              + next_month.strftime('%b. %Y') \
              + ' >**](/lifelogs/' + next_month.strftime('%Y/%m') \
              + '/index.html) &nbsp; &nbsp; |  &nbsp; &nbsp; '\
              + '[返回年历 **Back to Years ^**](/lifelogs/index.html)\n<br/>\n' \
              + '#### Logs 日志记录\n' \
              + '---\n'

    month_log_path = '%s/%s/%s/index.md' % (
        lifelog_dir,
        day.strftime('%Y'),
        day.strftime('%m')
    )

    import codecs
    with codecs.open(month_log_path, 'w', 'utf-8') as f:
        f.write(content)

    # years_log_path = '%s/index.md' % lifelog_dir
    years_log_path = '/Users/IceHe/Coding/Blog/icehe.blog.hexo/source/_posts/lifelogs.md'

    month2yue = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']

    import pymysql
    conn = pymysql.connect(
        user='test',
        password='88887777',
        database='life_log'
    )

    cursor = conn.cursor()

    sql = 'select stu_pct, spo_pct, was_pct from month_log where month_1st = "%s"' \
          % day.strftime('%Y/%m/%d')

    cursor.execute(sql)

    month_time_stat = cursor.fetchall()
    month_time_stat = [round(x) for x in month_time_stat[0]]

    cursor.close()
    conn.close()

    import codecs
    with codecs.open(years_log_path, 'a', 'utf-8') as f:
        f.write('%s. [%s月：月度关键词。](/lifelogs/%s/%s/index.html) 学 %s 动 %s 废 %s\n    <sup>%s: keywords.</sup>' % (
            day.month,
            month2yue[day.month],
            day.year,
            day.strftime('%m'),
            month_time_stat[0],
            month_time_stat[1],
            month_time_stat[2],
            day.strftime('%b')
        ))

    return True


def post_daylog_to_blog(day):

    notebook_name = day.strftime('%Y/%m')
    note_name = day.strftime('%y/%m/%d')

    ##############################
    # export Note
    ##############################
    import os
    print('Export Note:')
    html_export_path = '/Users/IceHe/Coding/Enex/lifelog/%s' \
                       % note_name.replace('/', '-')

    cmd = 'osascript /Users/IceHe/Coding/AppleScript/Evernote/note_export_html_with_nbname.scpt "%s" "%s" "%s"' % (
        note_name,
        notebook_name,
        html_export_path
    )

    os.system(cmd)
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
    note_title = re.findall(
        r'(?:<title>)([\s\S]*?)(?:</title>)',
        content,
        re.S
    )[0]

    output = re.findall(
        r'(?:<body[^>]*?>)([\s\S]*?)(?:</body>)',
        content,
        re.S
    )[0]

    # remove the part of Diary
    output = re.sub(
        r'(<div><b># Diary</b></div>[\s\S]*)',
        '',
        output,
        re.S
    )

    # 旧日志格式不同，需要用不同的规则识别
    target = re.findall(
        r'(?:总[\d\.]*?</div>)([\s\S]*)',
        output,
        re.S
    )[0]
    # print(output, '\n\n')
    # print(target)
    # output = re.sub(target, '', output, re.S)
    output = output.replace(target, '')

    ##############################
    # process Text Content
    ##############################
    prev_day = day - timedelta(days=1)
    next_day = day + timedelta(days=1)

    p_MdY = prev_day.strftime('%b. %d, %Y')
    n_MdY = next_day.strftime('%b. %d, %Y')

    p_Ymd = prev_day.strftime('%Y/%m/d%d')
    n_Ymd = next_day.strftime('%Y/%m/d%d')
    c_Ym = day.strftime('%Y/%m')

    output = 'title: ' + note_title + '\n' \
             + 'date: ' + day.strftime('%Y-%m-%d %H:%M:%S') + '\n' \
             + 'toc: false\n' \
             + '---\n' \
             + '[**< ' + p_MdY + '** - Prev 上一天](/lifelogs/' + p_Ymd \
             + '.html) &nbsp; &nbsp; | &nbsp; &nbsp; [下一天 Next - **' \
             + n_MdY + ' >**](/lifelogs/' + n_Ymd \
             + '.html) &nbsp; &nbsp; |  &nbsp; &nbsp; [返回月历 **Back to Month ^**](/lifelogs/' \
             + c_Ym + '/index.html)\n<br/>' \
             + output.replace('\n', '')

    ##############################
    # make dir of Life Log
    ##############################
    lifelog_dir = '/Users/IceHe/Coding/Blog/icehe.blog.hexo/source/lifelogs'

    from pathlib import Path
    cur_year_dir = '%s/%s' % (
        lifelog_dir,
        day.strftime('%Y')
    )

    if not Path(cur_year_dir).exists():
        os.mkdir(cur_year_dir)

    cur_month_dir = '%s/%s' % (
        cur_year_dir,
        day.strftime('%m')
    )

    if not Path(cur_month_dir).exists():
        os.mkdir(cur_month_dir)

    ##############################
    # output Post
    ##############################
    day_log_path = '%s/d%s.md' % (
        cur_month_dir,
        day.strftime('%d')
    )
    with codecs.open(day_log_path, 'w', 'utf-8') as f:
        f.write(output)

    ##############################
    # add link to Month Log page
    ##############################
    month_log_path = '%s/index.md' % cur_month_dir
    print(Path(month_log_path).exists())

    if not Path(month_log_path).exists():
        post_monthlog_to_blog(day, lifelog_dir)

    with codecs.open(month_log_path, 'a', 'utf-8') as f:
        f.write('%s. [%s](/lifelogs/%s/%s/d%s.html)\n' % (
            day.day,
            note_title,
            day.year,
            day.strftime('%m'),
            day.strftime('%d')
        ))


def post_time_stat_to_blog(day):

    cur_month_1st = datetime(day.year, day.month, 1)

    notebook_name = cur_month_1st.strftime('%Y/%m')
    note_name = cur_month_1st.strftime('%Y/%m')

    ##############################
    # export Note
    ##############################
    import os
    print('Export Note:')
    html_export_path = '/Users/IceHe/Coding/Enex/lifelog_month_stat/%s' \
                       % note_name.replace('/', '-')

    cmd = 'osascript /Users/IceHe/Coding/AppleScript/Evernote/note_export_html_with_nbname.scpt "%s" "%s" "%s"' % (
        note_name,
        notebook_name,
        html_export_path
    )

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
    with codecs.open('%s/%s' % (html_export_path, html_file_name), 'r', 'utf-8') as f:
        content = f.read()

    import re
    note_title = re.findall(
        r'(?:<title>)([\s\S]*?)(?:</title>)',
        content,
        re.S
    )[0]

    output = re.findall(
        r'(?:<body[^>]*?>)([\s\S]*?)(?:</body>)',
        content,
        re.S
    )[0]

    ##############################
    # process Text Content
    ##############################
    cur_month_last_day = cur_month_1st + timedelta(
        days=calendar.monthrange(day.year, day.month)[1] - 1
    )

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
    lifelog_dir = '/Users/IceHe/Coding/Blog/icehe.blog.hexo/source/lifelogs'
    cur_year_dir = '%s/%s' % (lifelog_dir, day.strftime('%Y'))
    cur_month_dir = '%s/%s' % (cur_year_dir, day.strftime('%m'))
    time_stat_path = '%s/time_stat.md' % cur_month_dir

    with codecs.open(time_stat_path, 'w', 'utf-8') as f:
        f.write(output)

    ##############################
    # add link to Month Log page
    ##############################
    month_log_path = '%s/index.md' % cur_month_dir
    with codecs.open(month_log_path, 'a', 'utf-8') as f:
        f.write('32. [**Summary %s**](/lifelogs/%s/%s/time_stat.html)\n' % (
            note_title,
            day.year,
            day.strftime('%m')
        ))

    ##############################
    # add Time Stat Brief to Month Log Title
    ##############################
    with codecs.open(month_log_path, 'r', 'utf-8') as f:
        month_log = f.read()

    month_index_title = re.findall(
        r'((title: \d\d\d\d/\d\d)([^\n]*))',
        month_log,
        re.S
    )[0]
    print(month_index_title)

    import pymysql
    conn = pymysql.connect(
        user='test',
        password='88887777',
        database='life_log'
    )
    cursor = conn.cursor()

    sql = 'select stu_pct, spo_pct, was_pct from month_log where month_1st = "%s"' \
          % day.strftime('%Y/%m/%d')

    cursor.execute(sql)

    month_time_stat = cursor.fetchall()
    month_time_stat = [round(x) for x in month_time_stat[0]]

    new_month_index_title = '%s stu%s spo%s was%s' % (
        month_index_title[1],
        month_time_stat[0],
        month_time_stat[1],
        month_time_stat[2]
    )

    cursor.close()
    conn.close()

    month_log = month_log.replace(month_index_title[0], new_month_index_title)
    with codecs.open(month_log_path, 'w', 'utf-8') as f:
        f.write(month_log)


if __name__ == '__main__':

    today = datetime.now()

    last_month_last_day = datetime(today.year, today.month, 1) - timedelta(days=1)

    last_month_1st = last_month_last_day - timedelta(
        days=calendar.monthrange(last_month_last_day.year, last_month_last_day.month)[1] - 1
    )

    print(last_month_1st)
    print(last_month_last_day)

    day = last_month_1st
    while day <= last_month_last_day:
        post_daylog_to_blog(day)
        day += timedelta(days=1)

    post_time_stat_to_blog(last_month_1st)
