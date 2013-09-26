# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from msgpack import packb, unpackb

from aps.base import get_timestamp, get_uuid
from aps.version import APS_VERSION



class APSMessage(object):

    def __init__(self):
        self.id = get_uuid()
        self.timestamp = get_timestamp()

    def __iter__(self):
        raise NotImplementedError()


class APSRequest(APSMessage):

    expire = 1000

    def __init__(self, method, params=list(), expire=None):
        super(APSRequest, self).__init__()
        self.method = method
        self.params = params
        self.expire = expire or APSRequest.expire
        self.extra_frames = list()

    def __iter__(self):
        return iter(self._to_list())

    def __repr__(self):
        return "#<aps.messageAPS.Request \"%s %s\">" % (self.method, self.id)

    def _to_list(self):
        ret = list()
        ret.append(APS_VERSION)
        ret.append(packb([self.id, self.timestamp, self.expire]))
        if type(self.method) == unicode:
            ret.append(self.method.encode('UTF-8'))
        else:
            ret.append(self.method)
        ret.append(packb(self.params))

        if len(self.extra_frames) > 0:
            for frame in self.extra_frames:
                ret.append(packb(frame))

        return ret

    def add_extra_frame(self, frame):
        self.extra_frames.append(frame)


class APSReply(APSMessage):

    def __init__(self, status, body):
        super(APSReply, self).__init__()
        self.status = status
        self.body = body
        self.extra_frames = list()

    def __iter__(self):
        return iter(self._to_list())

    def __repr__(self):
        return "#<aps.message.APSReply \"%s %s\">" % (self.status, self.id)

    def _to_list(self):
        ret = list()
        ret.append(APS_VERSION)
        ret.append(packb([self.id, self.timestamp, self.status]))
        ret.append(packb(self.body))

        if len(self.extra_frames) > 0:
            for frame in self.extra_frames:
                ret.append(packb(frame))

        return ret

    def add_extra_frame(self, frame):
        self.extra_frames.append(frame)

    @staticmethod
    def from_frames(frames):
        version = frames[0]
        _id, timestamp, status = unpackb(frames[1])
        body = unpackb(frames[2])
        extra_frames = list()
        if len(frames) > 3:
            for frame in frames[3:]:
                extra_frames.append(unpackb(frame))

        message = APSReply.__new__(APSReply)
        message.id = _id
        message.timestamp = timestamp
        message.status = status
        message.body = body
        message.extra_frames = extra_frames
        return message
