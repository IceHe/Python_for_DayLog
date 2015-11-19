#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'IceHe'


# itertools
import itertools

# count
naturals = itertools.count(1)
# for n in naturals: # can't stop
#     print(n)


# cycle
cs = itertools.cycle('ABC')
# for c in cs: # can't stop
#     print(c)


# repeat
ns = itertools.repeat('A', 3)
for n in ns:
    print(n)
print()


# takewhile()
naturals = itertools.count(1)
ns = itertools.takewhile(lambda x: x <= 10, naturals)
for n in ns:
    print(n)

naturals = itertools.count(1)
ns = itertools.takewhile(lambda x: x <= 10, naturals)
print(list(ns))
print()


# chain()
for c in itertools.chain('ABC', 'XYZ'):
    print(c)
print()


# groupby()
for key, group in itertools.groupby('AABBBCCA'):
    print(key, list(group))
print()



# XML
from xml.parsers.expat import ParserCreate

class DefaultSaxHandler(object):
    def start_elem(self, name, attrs):
        print('sax:start_elem: %s, attrs: %s'
              % (name, str(attrs)))

    def end_elem(self, name):
        print('sax:end_elem: %s' % name)

    def char_data(self, text):
        print('sax:char_data: %s' % text)

handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_elem
parser.EndElementHandler = handler.end_elem
parser.CharacterDataHandler = handler.char_data

parser.Parse(r'''<?xml version="1.0"?>
<ol>
    <li><a href="/python">Python</a></li>
    <li><a href="/ruby">Ruby</a></li>
</ol>
''')
print()



# HTMLParser
from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)

    def handle_data(self, data):
        print(data)

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('$#%s;' % name)

parser = MyHtmlParser()
parser.feed('''<html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
</body></html>''')
print()



# urllib
from urllib import request

print('GET1')
with request.urlopen('https://api.douban.com/v2/book/2129650') as f:
    data = f.read()
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
        print('Data:', data.decode('utf-8'))
print()


print('GET2')
req = request.Request('http://www.douban.com/')
req.add_header('User-Agent',
               'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))
print()


print('POST')
from urllib import parse
print('Login to weibo.cn...')
email = input('Email: ')
passwd = input('Password: ')
login_data = parse.urlencode([
    ('username', email),
    ('password', passwd),
    ('entry', 'mweibo'),
    ('client_id', ''),
    ('savestate', '1'),
    ('ec', ''),
    ('pagerefer', 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
])

req = request.Request('https://passport.weibo.cn/sso/login')
req.add_header('Origin', 'https://passport.weibo.cn')
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
req.add_header('Referer', 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')

with request.urlopen(req, data = login_data.encode('utf-8')) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))
print()


# handler
# proxy_handler = urllib.request.ProxyHandler({'http': 'http://www.example.com:3128/'})
# proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
# proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
# opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
# with opener.open('http://www.example.com/login.html') as f:
#     pass

