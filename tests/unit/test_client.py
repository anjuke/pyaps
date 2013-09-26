# -*- coding: utf-8 -*-
from unittest import TestCase
from os.path import abspath, dirname
import subprocess
import zmq
import aps
from aps import get_timestamp
from aps.client import APSClient, wait_for_replies, fetch_reply, shutdown

class ClientTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        cls.client = APSClient('tcp://127.0.0.1:5000')
        cwd = dirname(abspath(__file__))
        cls.p = subprocess.Popen('python server.py', shell=True, cwd=cwd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    @classmethod
    def tearDownClass(cls):
        shutdown()
        cls.p.kill()

    def test_client_class(self):
        self.assertIsInstance(self.client, APSClient)

    def test_client_socket(self):
        self.assertIsInstance(self.client.socket, zmq.Socket)
        self.assertEqual(self.client.socket.type, zmq.DEALER)

    def test_client_start_request(self):
        id = self.client.start_request("ping", list())
        self.assertTrue(id is not None)
        self.assertEqual(len(aps.client.requests), 1)

    def test_client_wait_for_replies(self):
        wait_for_replies(100)
        self.assertTrue(len(aps.client.responses) > 0)

    def test_client_fetch_reply(self):
        client = APSClient('tcp://127.0.0.1:5000')
        seq = client.start_request("ping", list())
        wait_for_replies(1000)
        reply, extra_frames = fetch_reply(seq)
        self.assertEqual(reply, 'pong')
