#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'

if __name__ == '__main__':

    import sys

    job_report_path = sys.argv[1]
    old_date_str = sys.argv[2]
    new_date_str = sys.argv[3]

    import codecs

    with codecs.open(job_report_path, 'r', 'utf-8') as f:
        content = f.read()

    content = content.replace(old_date_str, new_date_str)

    with codecs.open(job_report_path, 'w', 'utf-8') as f:
        f.write(content)
