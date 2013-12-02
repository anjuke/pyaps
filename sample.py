# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import aps


# set default timeout
aps.default_timeout = 0.1

# connect to an APS endpoint
aps.connect('tcp://127.0.0.1:8964')

def callback(result, status):
    print("[{}] {}".format(status, result))

# with callback
hdl1 = aps.start_request(method='time', callback=callback)

# with parameters
hdl2 = aps.start_request(method='echo', 'Hello World')
hdl3 = aps.start_request(method='sleep', 2)

hdl4 = aps.start_request(method='time')

for i in range(100):
    aps.start_request(method='time')

# 10ms for first reply
replies = aps.wait_for_replies(hdl1, timeout=0.01)
print(replies)

# default timeout
replies = aps.wait_for_replies(hdl2, hdl4)
print(replies)

# return already received replies without wait
replies = aps.wait_for_replies(timeout=0)
print(replies)

# wait for another 100ms
replies = aps.wait_for_replies()
print(replies)

def check_status(result, status):
    if status == 200:
        print(result)

aps.start_request(method='.status', callback=check_status)

replies = aps.wait_for_replies(timeout=-1)
print(replies)
