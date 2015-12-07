#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'


from datetime import datetime, timedelta
import calendar


def post_monthlog_to_blog(day, lifelog_dir):

    prev_month_last_day =  day - timedelta(days = day.day)
    prev_month = prev_month_last_day - timedelta(days = prev_month_last_day.day - 1)
    next_month = day + timedelta(days = calendar.monthrange(day.year, day.month)[1] - day.day + 1)

    content = 'title: ' + day.strftime('%Y/%m') + '\n' \
              + 'date: ' + day.strftime('%Y-%m-01 00:00:00') + '\n' \
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

    month_log_path = '%s/%s/%s/index.md' % (lifelog_dir, day.strftime('%Y'), day.strftime('%m'))

    import codecs
    with codecs.open(month_log_path, 'w', 'utf-8') as f:
        f.write(content)

    years_log_path = '%s/index.md' % lifelog_dir

    month2yue = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']

    import codecs
    with codecs.open(years_log_path, 'a', 'utf-8') as f:
        f.write('%s. [%s月：月度关键词。 %s: keywords.](/lifelogs/%s/%s/index.html)\n'
                % (day.month, month2yue[day.month], day.strftime('%b'), day.year, day.strftime('%m')))

    return True



def post_daylog_to_blog(day):

    notebook_name = day.strftime('%Y/%m')
    note_name = day.strftime('%y/%m/%d')


    ##############################
    # export Note
    ##############################
    import os
    print('Export Note:')
    html_export_path = '/Users/IceHe/Coding/Enex/lifelog/' + note_name.replace('/', '-')
    cmd = 'osascript /Users/IceHe/Coding/AppleScript/Evernote/note_export_html_with_nbname.scpt "'\
              + note_name + '" "' + notebook_name + '" "' + html_export_path + '"'
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
    note_title = re.findall(r'(?:<title>)([\s\S]*?)(?:<\/title>)', content, re.S)[0]
    output = re.findall(r'(?:<body[^>]*?>)([\s\S]*?)(?:<\/body>)', content, re.S)[0]

    # remove the part of Diary
    output = re.sub(r'(<div><b># Diary<\/b><\/div>[\s\S]*)', '', output, re.S)

    # 旧日志格式不同，需要用不同的规则识别
    target = re.findall(r'(?:总[\d\.]*?<\/div>)([\s\S]*)', output, re.S)[0]
    # print(output, '\n\n')
    # print(target)
    # output = re.sub(target, '', output, re.S)
    output = output.replace(target, '')


    ##############################
    # process Text Content
    ##############################
    prev_day = day - timedelta(days = 1)
    next_day = day + timedelta(days = 1)

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
             + '.html) &nbsp; &nbsp; |  &nbsp; &nbsp; [返回月历 **Back to Month ^**](/lifelogs/'\
             + c_Ym + '/index.html)\n<br/>' \
             + output.replace('\n', '')


    ##############################
    # make dir of Life Log
    ##############################
    lifelog_dir = '/Users/IceHe/Coding/Blog/icehe.blog.hexo/source/lifelogs'

    from pathlib import Path
    cur_year_dir = lifelog_dir + '/' + day.strftime('%Y')
    if not Path(cur_year_dir).exists():
        os.mkdir(cur_year_dir)

    cur_month_dir = cur_year_dir + '/' + day.strftime('%m')
    if not Path(cur_month_dir).exists():
        os.mkdir(cur_month_dir)


    ##############################
    # output Post
    ##############################
    day_log_path = '%s/d%s.md' % (cur_month_dir, day.strftime('%d'))
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
        f.write('%s. [%s](/lifelogs/%s/%s/d%s.html)\n' % (day.day, note_title, day.year, day.strftime('%m'), day.strftime('%d')))


if __name__ == '__main__':
    # exit(0) # SWITCH
    day = datetime(2015, 11, 1)
    while day < datetime(2015, 12, 1):
        post_daylog_to_blog(day)
        day += timedelta(days = 1)
    # post_daylog_to_blog(day)
