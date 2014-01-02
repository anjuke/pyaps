# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase

from msgpack import packb


class APSMessageTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_aps_version(self):
        from aps.message import VERSION
        self.assertEqual(b'APS12', VERSION)

    def test_aps_empty(self):
        from aps.message import EMPTY
        self.assertEqual(b'', EMPTY)

    def test_aps_request(self):
        from aps.message import APSRequest
        from aps.util import get_timestamp
        envelope = ['test envelope']
        sequence = 1
        timestamp = get_timestamp()
        expiry = None
        method = 'sp.up'
        params = ['p1', 'p2']

        request = APSRequest(envelope=envelope,
                             sequence=sequence,
                             timestamp=timestamp,
                             expiry=expiry,
                             method=method,
                             params=params)

        self.assertEqual(request.envelope, envelope)
        self.assertEqual(request.sequence, sequence)
        self.assertEqual(request.timestamp, timestamp)
        self.assertEqual(request.expiry, expiry)
        self.assertEqual(request.method, method)
        self.assertEqual(request.params, params)

    def test_aps_request_frames(self):
        from aps.message import APSRequest, EMPTY, VERSION
        from aps.util import get_timestamp
        envelope = ['test request envelope']
        sequence = 1
        timestamp = get_timestamp()
        expiry = None
        method = 'sp.up'
        params = ['p1', 'p2']
        extras = ['ex1', 'ex2', ('ex3', ('ex4', 'ex5'))]

        request = APSRequest(envelope=envelope,
                             sequence=sequence,
                             timestamp=timestamp,
                             expiry=expiry,
                             method=method,
                             params=params,
                             extras=extras)

        from aps.util import ensure_bytes
        _frames = map(ensure_bytes, envelope)
        _frames.append(EMPTY)
        _frames.append(VERSION)
        _frames.append(packb((sequence, timestamp, expiry)))
        _frames.append(ensure_bytes(method))
        _frames.append(packb(params))
        _frames.extend(map(packb, extras))

        self.assertEqual(request.frames, _frames)

    def test_aps_reply(self):
        from aps.message import APSReply
        from aps.util import get_timestamp
        envelope = ['test reply envelope']
        sequence = 1
        timestamp = get_timestamp()
        status = 200
        result = 'ok!!!'
        extras = ['ex1', ('ex2', ('ex3', 'ex4')), 'ex5']

        reply = APSReply(envelope=envelope,
                         sequence=sequence,
                         timestamp=timestamp,
                         status=status,
                         result=result,
                         extras=extras)

        self.assertEqual(reply.envelope, envelope)
        self.assertEqual(reply.sequence, sequence)
        self.assertEqual(reply.timestamp, timestamp)
        self.assertEqual(reply.status, status)
        self.assertEqual(reply.result, result)
        self.assertEqual(reply.extras, extras)

    def test_aps_reply_frames(self):
        from aps.message import APSReply, EMPTY, VERSION
        from aps.util import get_timestamp, ensure_bytes
        envelope = ['test reply envelope']
        sequence = 1
        timestamp = get_timestamp()
        status = 200
        result = 'ok!!!'
        extras = ['ex1', ('ex2', ('ex3', 'ex4')), 'ex5']

        reply = APSReply(envelope=envelope,
                         sequence=sequence,
                         timestamp=timestamp,
                         status=status,
                         result=result,
                         extras=extras)

        _frames = map(ensure_bytes, envelope)
        _frames.append(EMPTY)
        _frames.append(VERSION)
        _frames.append(packb((sequence, timestamp, status)))
        _frames.append(packb(result))
        _frames.extend(map(packb, extras))

        self.assertEqual(reply.frames, _frames)

    def test_aps_request_from_frames(self):
        from aps.message import APSRequest, EMPTY, VERSION
        from aps.util import get_timestamp, ensure_bytes
        envelope = ['test request envelope']
        sequence = 1
        timestamp = get_timestamp()
        expiry = None
        method = 'sp.up'
        params = ['p1', 'p2']
        extras = ['ex1', 'ex2', ['ex3', ['ex4', 'ex5']]]

        _frames = map(ensure_bytes, envelope)
        _frames.append(EMPTY)
        _frames.append(VERSION)
        _frames.append(packb((sequence, timestamp, expiry)))
        _frames.append(ensure_bytes(method))
        _frames.append(packb(params))
        _frames.extend(map(packb, extras))

        request = APSRequest(frames=_frames)

        self.assertEqual(request.envelope, envelope)
        self.assertEqual(request.sequence, sequence)
        self.assertEqual(request.timestamp, timestamp)
        self.assertEqual(request.expiry, expiry)
        self.assertEqual(request.method, method)
        self.assertEqual(request.params, params)
        self.assertEqual(request.extras, extras)

    def test_aps_reply_from_frames(self):
        from aps.message import APSReply, EMPTY, VERSION
        from aps.util import get_timestamp, ensure_bytes
        envelope = ['test reply envelope']
        sequence = 1
        timestamp = get_timestamp()
        status = 200
        result = 'ok!!!'
        extras = ['ex1', ['ex2', ['ex3', 'ex4']], 'ex5']

        _frames = map(ensure_bytes, envelope)
        _frames.append(EMPTY)
        _frames.append(VERSION)
        _frames.append(packb((sequence, timestamp, status)))
        _frames.append(packb(result))
        _frames.extend(map(packb, extras))

        reply = APSReply(frames=_frames)

        self.assertEqual(reply.envelope, envelope)
        self.assertEqual(reply.sequence, sequence)
        self.assertEqual(reply.timestamp, timestamp)
        self.assertEqual(reply.status, status)
        self.assertEqual(reply.result, result)
        self.assertEqual(reply.extras, extras)
