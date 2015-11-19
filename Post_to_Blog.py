#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    note_name = input('note_name: ')
    # note_name = r't_post'
    print('input = [[' + note_name + ']]')

    from datetime import datetime
    today = datetime.now()
    timestamp_str = today.strftime('%y%m%d_%H%M%S')
    print(timestamp_str)


    import random
    import re
    html_export_path = '/Users/IceHe/Coding/Enex/post/'\
                       + re.sub(r'[\\\\/&\<\>\\?\\!]', '_', note_name)\
                       + '_' + timestamp_str \
                       + '_' + str(random.randint(100, 999))

    print(html_export_path)


    ##############################
    # export Note & get Content
    ##############################
    import os
    print('Export Note:')
    os.system('osascript /Users/IceHe/Coding/AppleScript/Evernote/note_export_html.scpt "'
              + note_name + '" "' + html_export_path + '"')

    import codecs
    with codecs.open(html_export_path + '/' + note_name + '.html', 'r', 'utf-8') as f:
        content = f.read()

    import re
    content = re.findall(r'(?:<body[^>]*?)([\s\S]*?)(?:<\/body>)', content, re.S)[0]

    print(content)


    ##############################
    # process Text Content
    ##############################
    content = 'title: ' + note_name + '\n' \
              + 'date: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n' \
              + 'tags: [Latest]' + '\n' \
              + 'categories: [Uncatedgoried]' + '\n' \
              + 'description: Latest Post\n' \
              + '---\n' + content.replace('\n', '')


    ##############################
    # upload Attachments & Image
    ##############################
    img_matches = re.findall(r'(?:<img src=")(' + note_name + r'\.resources\/([^"]*))(?:[\s\S]\/>)?', content, re.S)
    print(img_matches)

    att_matches = re.findall(r'(?:<a href=")(' + note_name + r'\.resources\/([^"]*))(?:">[\s\S]*?<\/a>)?', content, re.S)
    print(att_matches)


    from pathlib import Path
    res_ori_path = html_export_path + '/' + note_name + '.resources/'
    print(res_ori_path)
    print(Path(res_ori_path).exists())


    img_path = '/Users/IceHe/Coding/Blog/ice-blog-img/' + note_name + '/'
    att_path = '/Users/IceHe/Coding/Blog/ice-blog-att/' + note_name + '/'
    if not Path(img_path).exists():
        os.mkdir(img_path)
    if not Path(att_path).exists():
        os.mkdir(att_path)


    import shutil
    for img in img_matches:
        shutil.copy(res_ori_path + img[1], img_path + img[1])
    for att in att_matches:
        shutil.copy(res_ori_path + att[1], att_path + att[1])


    img_cloud = 'http://7vzp68.com1.z0.glb.clouddn.com/'
    att_cloud = 'http://7vzp67.com1.z0.glb.clouddn.com/'

    from urllib.parse import quote
    for img in img_matches:
        content = content.replace(img[0], img_cloud + quote(note_name) + '/' + img[1])
    for att in att_matches:
        content = content.replace(att[0], att_cloud + quote(note_name) + '/' + att[1])

    print(content)


    ##############################
    # output Post
    ##############################
    post_path = '/Users/IceHe/Coding/Blog/icehe.blog.hexo/source/_posts/LATEST/' + note_name + '.md'

    with codecs.open(post_path, 'w', 'utf-8') as f:
        f.write(content)
