# -*- coding: utf-8 -*-
from time import time

from msgpack import packb, unpackb

from aps._compat import str_types, bytes_types



VERSION = r'APS1.2'
EMPTY = r''

class APSRequest(object):
    """Base APS Request messsage class
    """

    def __init__(self, frames=None, **kwargs):
        if frames:
            self._frames = frames
            try:
                self._sep = frames.index(EMPTY)
            except:
                self._sep = -1
            return

        self.envelope  = kwargs.pop('envelope', None)
        self.version   = kwargs.pop('version', VERSION)
        self.sequence  = kwargs.pop('sequence', None)
        self.timestamp = kwargs.pop('timestamp', None)
        self.expiry    = kwargs.pop('expiry', None)
        self.method    = kwargs.pop('method', None)
        self.params    = kwargs.pop('params', None)
        self.extras    = kwargs.pop('extras', None)

    def __repr(self):
        return '''<#APSRequest {} {} {}>'''.format(self.sequence,
                                                   self.method, self.status)

    def inspect(self):
        return '''APSRequest:
   envelope: %r
    version: %r
   sequence: %r
  timestamp: %r
     expiry: %r
     method: %r
     params: %r
     extras: %r''' % (
        self.envelope,
        self.version,
        self.sequence, self.timestamp, self.expiry,
        self.method, self.params,
        self.extras)

    def __getattr__(self, attr):
        assert self._frames

        if attr == 'envelope':
            if self._sep >= 0:
                self.envelope = self._frames[:self._sep]
            else:
                self.envelope = None
            return self.envelope

        if attr == 'version':
            self.version = self._frames[self._sep + 1]
            return self.version

        if attr == 'sequence' or attr == 'timestamp' or attr == 'expiry':
            self.sequence, self.timestamp, self.expiry = unpackb(
                    self._frames[self._sep + 2])
            if attr == 'sequence':
                return self.sequence
            if attr == 'timestamp':
                return self.timestamp
            if attr == 'expiry':
                return self.expiry

        if attr == 'method':
            self.method = self._frames[self._sep + 3]
            return self.method

        if attr == 'params':
            self.params = unpackb(self._frames[self._sep + 4])
            return self.params

        if attr == 'extras':
            if len(self._frames) > self._sep + 5:
                self.extras = []
                for extra in self._frames[self._sep + 5]:
                    self.extras.append(unpackb(extra))
            else:
                self.extras = None
            return self.extras

    @property
    def frames(self):
        if hasattr(self, '_frames'):
            return self._frames

        if self.envelope is not None:
            frames = self.envelope[:]
            frames.append(EMPTY)
        else:
            frames = [EMPTY]
        frames.append(self.version)
        frames.append(packb((self.sequence, self.timestamp,
                                     self.expiry)))
        if type(self.method) in str_types:
            _method = self.method.encode('UTF-8')
            frames.append(_method)
        else:
            frames.append(self.method)
        frames.append(packb(self.params))
        if self.extras is not None:
            for extra in self.extras:
                frames.append(packb(extra))
        return frames

class APSReply(object):
    """Base APS Reply message class
    """

    def __init__(self, frames=None, **kwargs):
        if frames:
            self._frames = frames
            try:
                self._sep = frames.index(EMPTY)
            except:
                self._sep = -1
            return

        self.envelope  = kwargs.pop('envelope', None)
        self.version   = kwargs.pop('version', VERSION)
        self.sequence  = kwargs.pop('sequence', None)
        self.timestamp = kwargs.pop('timestamp', None)
        self.status    = kwargs.pop('status', None)
        self.result    = kwargs.pop('result', None)
        self.extras    = kwargs.pop('extras', None)

    def __repr__(self):
        return '''<#APSReply {} {}>'''.format(self.sequence,
                                              self.status)

    def inspect(self):
        return '''APSReply:
   envelope: %r
    version: %r
   sequence: %r
  timestamp: %r
     status: %r
     result: %r
     extras: %r''' % (
        self.envelope,
        self.version,
        self.sequence, self.timestamp, self.status,
        self.result,
        self.extras)

    def __getattr__(self, attr):
        assert self._frames

        if attr == 'envelope':
            if self._sep >= 0:
                self.envelope = self._frames[:self._sep]
            else:
                self.envelope = None
            return self.envelope

        if attr == 'version':
            self.version = self._frames[self._sep + 1]
            return self.version

        if attr == 'sequence' or attr == 'timestamp' or attr == 'status':
            self.sequence, self.timestamp, self.status = unpackb(
                    self._frames[self._sep + 2])
            if attr == 'sequence':
                return self.sequence
            if attr == 'timestamp':
                return self.timestamp
            if attr == 'status':
                return self.status

        if attr == 'result':
            self.result = unpackb(self._frames[self._sep + 3])
            return self.result

        if attr == 'extras':
            if len(self._frames) > self._sep + 4:
                self.extras = []
                for extra in self._frames[self._sep + 4]:
                    self.extras.append(unpackb(extra))
            else:
                self.extras = None
            return self.extras

    @property
    def frames(self):
        if hasattr(self, '_frames'):
            return self._frames

        if self.envelope is not None:
            frames = self.envelope[:]
            frames.append(r'')
        else:
            frames = []
        frames.append(self.version)
        frames.append(packb((self.sequence, self.timestamp,
                                     self.status)))
        frames.append(packb(self.result))
        if self.extras is not None:
            for extra in self.extras:
                frames.append(packb(extra))
        return frames
