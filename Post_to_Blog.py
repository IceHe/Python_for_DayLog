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
    html_export_path = '/Users/IceHe/Documents/Enex/post/%s_%s_%s' % (
        re.sub(r'[\\\\/&<>\\?\\!]', '_', note_name),
        timestamp_str,
        str(random.randint(100, 999))
    )

    print(html_export_path)

    ##############################
    # export Note & get Content
    ##############################
    import os
    print('Export Note:')
    os.system('osascript /Users/IceHe/Documents/AppleScript/Evernote/note_export_html.scpt "%s" "%s"' % (
        note_name,
        html_export_path
    ))

    import codecs
    with codecs.open('%s/%s.html' % (html_export_path, note_name), 'r', 'utf-8') as f:
        content = f.read()

    import re
    content = re.findall(
        r'(?:<body[^>]*?)([\s\S]*?)(?:</body>)',
        content,
        re.S
    )[0]

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
    img_matches = re.findall(
        r'(?:<img src=")(%s\.resources/([^"]*))(?:[\s\S]/>)?' % note_name,
        content,
        re.S
    )
    print(img_matches)

    att_matches = re.findall(
        r'(?:<a href=")(%s\.resources/([^"]*))(?:">[\s\S]*?</a>)?' % note_name,
        content,
        re.S
    )
    print(att_matches)

    from pathlib import Path
    res_ori_path = '%s/%s.resources/' % (html_export_path, note_name)
    print(res_ori_path)
    print(Path(res_ori_path).exists())

    img_path = '/Users/IceHe/Documents/Blog/ice-blog-img/%s/' % note_name
    att_path = '/Users/IceHe/Documents/Blog/ice-blog-att/%s/' % note_name
    if not Path(img_path).exists():
        os.mkdir(img_path)
    if not Path(att_path).exists():
        os.mkdir(att_path)

    import shutil
    for img in img_matches:
        shutil.copy(
            res_ori_path + img[1],
            img_path + img[1]
        )
    for att in att_matches:
        shutil.copy(
            res_ori_path + att[1],
            att_path + att[1]
        )

    img_cloud = 'http://7vzp68.com1.z0.glb.clouddn.com/'
    att_cloud = 'http://7vzp67.com1.z0.glb.clouddn.com/'

    from urllib.parse import quote
    for img in img_matches:
        content = content.replace(
            img[0],
            '%s%s/%s' % (
                img_cloud,
                quote(note_name),
                img[1]
            )
        )
    for att in att_matches:
        content = content.replace(
            att[0],
            '%s%s/%s' % (
                att_cloud,
                quote(note_name),
                '/' + att[1]
            )
        )

    print(content)

    ##############################
    # output Post
    ##############################
    post_path = '/Users/IceHe/Documents/Blog/icehe.blog.hexo/source/_posts/LATEST/%s.md' % note_name

    with codecs.open(post_path, 'w', 'utf-8') as f:
        f.write(content)
