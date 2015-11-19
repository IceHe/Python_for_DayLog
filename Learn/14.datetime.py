#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# datetime
from datetime import datetime
now = datetime.now()
print(now)
print(type(now))
print()


# specified datetime
dt = datetime(2015, 9, 10, 11, 5)
print(dt)
print()


# datetime to timestamp
print(datetime(1970, 1, 1, 0, 0).timestamp())
print(dt.timestamp())
print(datetime.now().timestamp())
print()


# timestamp to datetime
t = 1429417200.0
print(datetime.fromtimestamp(t))
print(datetime.utcfromtimestamp(t))
print()


# str to datetime
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday)
print()


# datetime to str
print(now.strftime('%a, %b %d %H:%M'))
print()


# calculate datetime
from datetime import timedelta
print(now - timedelta(hours = 10))
print(now - timedelta(days = 1))
print(now - timedelta(minutes = 45))
print()


# localtime to utctime
from datetime import timezone
tz_utc_8 = timezone(timedelta(hours = 8))
print(now.replace(tzinfo = tz_utc_8))
print()


# timzone
utc_dt = datetime.utcnow().replace(tzinfo = timezone.utc)
print(utc_dt)

bj_dt = utc_dt.astimezone(timezone(timedelta(hours = 8)))
print(bj_dt)

tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours = 9)))
print(tokyo_dt)

tokyo_dt2 = bj_dt.astimezone(timezone(timezone(hours = 9)))
print(tokyo_dt2)
print()
