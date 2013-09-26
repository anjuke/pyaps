from unittest import TestCase
from datetime import datetime
from os.path import abspath, dirname
import subprocess
from msgpack import unpackb
from aps.message import APSMessage, APSRequest, APSReply
from aps.version import APS_VERSION


class MessageTestCase(TestCase):

    def setUp(self):
        cwd = dirname(abspath(__file__))
        self.p = subprocess.Popen('python server.py', shell=True, cwd=cwd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    def tearDown(self):
        self.p.send_signal(9)

    def test_message_class(self):
        msg = APSMessage()
        self.assertIsInstance(msg, APSMessage)

    def test_message_timestamp(self):
        msg = APSMessage()
        ts = msg.timestamp
        self.assertIsInstance(ts, float)
        self.assertTrue(ts > 0)
        self.assertTrue(len(str(int(ts))) == 13)

        _ = datetime.fromtimestamp(int(ts / 1000))
        now = datetime.now()

        self.assertEqual(_.year, now.year)
        self.assertEqual(_.month, now.month)
        self.assertEqual(_.day, now.day)
        self.assertEqual(_.hour, now.hour)
        self.assertEqual(_.minute, now.minute)

    def test_request_class(self):
        method_name = 'test_method'
        params = [1, 2]
        msg = APSRequest(method_name, params)
        self.assertIsInstance(msg, APSRequest)
        self.assertIsInstance(msg, APSMessage)

    def test_request_expire(self):
        method_name = 'test_method'
        params = [1, 2]
        msg = APSRequest(method_name, params)
        self.assertEqual(msg.expire, APSRequest.expire)

        msg = APSRequest(method_name, params, 2000)
        self.assertEqual(msg.expire, 2000)


    def test_request_timestamp(self):
        method_name = 'test_method'
        params = [1, 2]
        msg = APSRequest(method_name, params)

        ts = msg.timestamp
        self.assertIsInstance(ts, float)
        self.assertTrue(ts > 0)
        self.assertTrue(len(str(int(ts))) == 13)

        _ = datetime.fromtimestamp(int(ts / 1000))
        now = datetime.now()

        self.assertEqual(_.year, now.year)
        self.assertEqual(_.month, now.month)
        self.assertEqual(_.day, now.day)
        self.assertEqual(_.hour, now.hour)
        self.assertEqual(_.minute, now.minute)

    def test_request_method(self):
        method_name = 'test_method'
        params = [1, 2]
        msg = APSRequest(method_name, params)
        self.assertEqual(msg.method, method_name)

    def test_request_params(self):
        method_name = 'test_method'
        params = [1, 2]
        msg = APSRequest(method_name)
        self.assertEqual(msg.params, list())

        msg = APSRequest(method_name, params)
        self.assertEqual(msg.params, params)

    def test_request_extra_frames(self):
        method_name = 'test_method'
        params = [1, 2]
        msg = APSRequest(method_name)

        self.assertEqual(msg.extra_frames, list())

        msg.add_extra_frame('ext_frame1')
        self.assertEqual(msg.extra_frames, ['ext_frame1'])

        msg.add_extra_frame(2)
        self.assertEqual(msg.extra_frames, ['ext_frame1', 2])

        msg.add_extra_frame([4])
        self.assertEqual(msg.extra_frames, ['ext_frame1', 2, [4]])

    def test_request_to_list(self):
        method_name = 'test_method'
        params = [1, 2]
        msg = APSRequest(method_name)

        _ = list(msg)
        self.assertEqual(_[0], APS_VERSION)
        self.assertEqual(type(unpackb(_[1])), list)
        self.assertEqual(unpackb(_[1])[2], APSRequest.expire)
        self.assertEqual(_[2], method_name)
        self.assertEqual(unpackb(_[3]), list())
        with self.assertRaises(IndexError):
            _[4]

        msg = APSRequest(method_name, params)
        msg.add_extra_frame('4')
        msg.add_extra_frame([5])
        _ = list(msg)
        self.assertEqual(unpackb(_[3]), params)
        self.assertEqual(unpackb(_[4]), '4')
        self.assertEqual(unpackb(_[5]), [5])

    def test_reply_class(self):
        body = ''
        msg = APSReply(200, body)
        self.assertIsInstance(msg, APSReply)

    def test_reply_status(self):
        body = ''
        msg = APSReply(200, body)
        self.assertEqual(msg.status, 200)

    def test_reply_body(self):
        body = 'test body'
        msg = APSReply(200, body)
        self.assertEqual(msg.body, body)

        body = ['test_body_in_list']
        msg = APSReply(200, body)
        self.assertEqual(msg.body, body)

    def test_reply_extra_frames(self):
        body = 'test body'
        msg = APSReply(200, body)

        self.assertEqual(msg.extra_frames, list())

        msg.add_extra_frame('ext_frame1')
        self.assertEqual(msg.extra_frames, ['ext_frame1'])

        msg.add_extra_frame(2)
        self.assertEqual(msg.extra_frames, ['ext_frame1', 2])

        msg.add_extra_frame([4])
        self.assertEqual(msg.extra_frames, ['ext_frame1', 2, [4]])

    def test_reply_to_list(self):
        body = 'test body'
        msg = APSReply(200, body)
        self.assertEqual(msg.body, body)

        _ = list(msg)
        self.assertEqual(_[0], APS_VERSION)
        self.assertEqual(type(unpackb(_[1])), list)
        self.assertEqual(unpackb(_[1])[2], 200)
        self.assertEqual(unpackb(_[2]), body)
        with self.assertRaises(IndexError):
            _[3]

        body = 'test body'
        msg = APSReply(200, body)
        msg.add_extra_frame('4')
        msg.add_extra_frame([5])
        _ = list(msg)
        self.assertEqual(unpackb(_[3]), '4')
        self.assertEqual(unpackb(_[4]), [5])

    def test_reply_from_frames(self):
        body = 'test body'
        msg = APSReply(200, body)
        self.assertEqual(msg.body, body)

        frames = list(msg)
        msg2 = APSReply.from_frames(frames)
        self.assertIsInstance(msg2, APSReply)
        self.assertEqual(msg.body, body)
