# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from aps import APS
from aps.base import wait_for_replies, pending_requests



aps = APS()

# set default timeout
aps.default_timeout = 100

# connect to an APS endpoint
# aps.connect('tcp://127.0.0.1:8964')
aps.connect('tcp://192.168.1.62:8964')

# with callback
hdl1 = aps.start_request(method='time')

# with parameters
hdl2 = aps.start_request(method='echo', params=['Hello World'])
# hdl3 = aps.start_request(method='sleep', params=[1.1])

hdl3 = aps.start_request(method='time')

for i in range(50):
    aps.start_request(method='time')

# 10ms for first reply
replies = wait_for_replies(hdl1, timeout=10)
print(replies)

# default timeout
replies = wait_for_replies(hdl2, hdl3)
print(replies)

# return already received replies without wait
replies = wait_for_replies(timeout=0)
print(replies)

# wait for another 100ms
replies = wait_for_replies()
print(replies)

aps.start_request(method='.status')

replies = wait_for_replies(timeout=-1)
print(replies)
