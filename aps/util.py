# -*- coding: utf-8 -*-
from time import time
from uuid import uuid4


def get_uuid():
    """return uuid
    """
    return uuid4().hex

def get_timestamp():
    """get current unix timestamp in float
    """
    return time() * 1000
