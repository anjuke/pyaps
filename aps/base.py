# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import time
from uuid import uuid4
import zmq

def get_timestamp():
    return float(time() * 1000)

def get_uuid():
    return uuid4().hex

def aps_send_frames(socket, frames):
    socket.send_multipart(frames)

def aps_recv_frames(socket, noblock):
    if noblock:
        return socket.recv_multipart(zmq.NOBLOCK)
    else:
        return socket.recv_multipart()
