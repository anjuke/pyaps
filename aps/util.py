# -*- coding: utf-8 -*-
from time import time
from uuid import uuid4

from aps._compat import str_types, bytes_types



def get_uuid():
    """return uuid"""
    return uuid4().hex

def get_timestamp():
    """get current unix timestamp in float"""
    return time() * 1000

def ensure_bytes(text):
    """ensure return bytes"""
    if type(text) in str_types:
        return text.encode('UTF-8')
    return text
