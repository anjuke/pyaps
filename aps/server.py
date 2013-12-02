# -*- coding: utf-8 -*-

from functools import wraps

functions = {}

def aps_func(func):
    functions[func.__name__] = func


@aps_func
def dot_ping():
    return 'pong'


request_method = '.ping'
if request_method.startswith('.'):
    method = request_method.replace('.', 'dot_')
    func = functions.get(method)
    args = [1]
    print func(*args)
