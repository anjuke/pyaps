# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import zmq

from aps.message import APSReply
from aps.util import get_timestamp




default_timeout = 100
sockets = set()
pending_requests = {}
pending_replies = {}

poller = zmq.Poller()

def aps_send_frames(socket, frames):
    """APS sending frames, via zmq API

    Args:
        +socket+ is an ZMQ socket
        +frames+ list of frames
    """
    socket.send_multipart(frames)

def aps_recv_frames(socket):
    """APS receiving frames, via zmq API
    """
    return socket.recv_multipart(zmq.NOBLOCK)

def register_socket(socket):
    """register a socket to APS poller

    Args:
        +socket+ is an APS socket
    """
    poller.register(socket, zmq.POLLIN)
    sockets.add(socket)

def wait_for_replies(*handlers, **kwargs):
    """receive and fetch replies from all sockets

    Args:
        +handlers+ is list of handlers
        +timeout+ to receive the replies
    """
    timeout = kwargs.get('timeout', None) or default_timeout

    rv = {}
    callbacks = set()

    if len(handlers) == 0:
        pending = set(pending_requests.keys())
    else:
        pending = set(handlers)

    # already recevied
    for i in pending.copy():
        if i in pending_replies:
            reply, _ = pending_replies.get(i)
            rv[reply.sequence] = reply
            pending.remove(i)
            pending_requests.pop(reply.sequence)

    timelimit = True
    if timeout == -1:
        timelimit = False

    def _process(socket):
        frames = aps_recv_frames(socket)
        reply = APSReply(frames)
        _, callback = pending_requests.get(reply.sequence)
        if reply.sequence in pending:
            if callable(callback):
                callbacks.add((reply, callback))
            else:
                rv[reply.sequence] = reply
            pending.remove(reply.sequence)
            pending_requests.pop(reply.sequence)
        else:
            pending_replies[reply.sequence] = (reply, callback)

    while len(pending) > 0:
        _start = get_timestamp()

        if timeout == -1:
            events = {}
            for socket in sockets:
                events[socket] = zmq.POLLIN
        else:
            events = dict(poller.poll(timeout))

        for socket in sockets:
            if socket in events and events.get(socket) == zmq.POLLIN:
                try:
                    while True:
                        _process(socket)
                except zmq.error.Again:
                    pass

        _end = get_timestamp()
        timeout -= _end - _start
        if timelimit and timeout <= 0:
            break

    # callbacks
    # TODO: spawn callback with greenlet
    # for _ in callbacks:
    #     reply, callback = _
    #     callback(reply)
    return rv
