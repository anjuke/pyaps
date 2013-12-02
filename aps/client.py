# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import zmq
from time import time
import errno
from aps import aps_send_frames, aps_recv_frames, get_timestamp
from aps.message import APSReply, APSRequest

ctx = zmq.Context()
poller = zmq.Poller()
sockets = list()
requests = dict()
responses = dict()

def add_endpoint(endpoint):
    """
    add zmq endpoint to global sockets
    """
    socket = ctx.socket(zmq.DEALER)
    socket.setsockopt(zmq.LINGER, 1000)
    socket.connect(endpoint)
    poller.register(socket, zmq.POLLIN)
    sockets.append(socket)
    return socket

def _store_request(message):
    requests[message.id] = message

def _store_reply(message):
    responses[message.id] = message


def _process_reply(socket):
    return True

def send_message(socket, message, envelope=None):
    frames = [b''] + list(message)
    if type(envelope) == list and envelope:
        frames = envelope + frames
    _store_request(message)
    aps_send_frames(socket, frames)

def recv_message(socket, noblock=False):
    from aps.message import APSReply
    frames = aps_recv_frames(socket, noblock)
    try:
        pos = frames.index('')
    except ValueError:
        pos = 0
    return (frames[0:pos], APSReply.from_frames(frames[pos + 1:]))

def wait_for_replies(timeout, ids=None):
    start = get_timestamp()
    if ids:
        pending = ids
    else:
        pending = requests.keys()
    while len(pending) > 0:
        try:
            events = dict(poller.poll(timeout))

            for socket in sockets:
                if socket in events and events.get(socket) == zmq.POLLIN:
                    while True:
                        try:
                            envelope, message = recv_message(socket,
                                                             noblock=True)

                            _store_reply(message)
                            pending.remove(message.id)
                        except zmq.ZMQError as e:
                            if e.errno == errno.EAGAIN:
                                break
                            else:
                                pass

            end = get_timestamp()

            timeout -= end - start
            if timeout <= 0:
                break
            start = end

        except zmq.ZMQError as e:
            if e.errno == errno.EINTR:
                break
            else:
                pass

def fetch_reply(_id, keep=False):
    reply = responses.get(_id)
    if reply and not keep:
        del requests[_id]
        del responses[_id]

    if reply:
        return (reply.body, reply.extra_frames)

def shutdown():
    for socket in sockets:
        poller.unregister(socket)
        socket.close()
    ctx.term()

class APSClient(object):

    DEFAULT_TIMEOUT = 10000

    def __init__(self, endpoint):
        self.socket = add_endpoint(endpoint)

    def start_request(self, method, params=list(), expire=None,
                      extra_frames=None):
        """
        start sending a request message to APS service endpoint

        Args:
            +method+ is the method name
            +params+ is a list of parameters
            +expire+ is the message expire
            +extra_frames+ is a list of extra frames

        Returns:
            message uuid
        """
        expire = expire or APSClient.DEFAULT_TIMEOUT

        message = APSRequest(method, params, expire)

        if type(extra_frames) == list and extra_frames:
            message.extra_frames = extra_frames
        send_message(self.socket, message)
        return message.id
