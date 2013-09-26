#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno
import zmq
from msgpack import packb, unpackb
from time import time

def get_timestamp():
    return float(time() * 1000)

def main():
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind('tcp://*:5000')

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    while True:
        try:
            events = dict(poller.poll(1000))
            print 'polling %s' % events
        except zmq.ZMQError as e:
            if e.errno == errno.EINTR:
                break
            else:
                pass

        if socket in events and events.get(socket) == zmq.POLLIN:
            try:
                frames = socket.recv_multipart(zmq.NOBLOCK)
            except zmq.ZMQError as e:
                if e.errno == errno.EAGAIN:
                    # no more message to handle
                    break
                else:
                    pass

            _id = frames[0]
            try:
                i = frames.index(b'')
            except:
                pass

            version = frames[i + 1]
            seq, ts, expire = unpackb(frames[i + 2])
            method = frames[i + 3]
            params = unpackb(frames[i + 4])

            print version, seq, ts, expire, method, params

            if method == 'ping':
                # pong!

                reply = [_id, r'', 'APS12']
                reply.append(packb([seq, get_timestamp(), 200]))
                reply.append(packb('pong'))
                socket.send_multipart(reply)
                print 'reply sent'

if __name__ == '__main__':
    main()
