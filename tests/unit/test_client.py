# -*- coding: utf-8 -*-
from unittest import TestCase

import zmq

from aps import APS



class APSClientTestCase(TestCase):

    def setUp(self):
        self.aps = APS()

    def tearDown(self):
        pass

    def test_aps_class(self):
        self.assertIsInstance(self.aps, APS)

    def test_aps_connect(self):
        self.assertTrue(callable(self.aps.connect))

        sock = self.aps.connect('tcp://127.0.0.1:1234')
        self.assertIsInstance(sock, zmq.Socket)

    def test_aps_start_request(self):
        self.assertTrue(callable(self.aps.start_request))

        sock = self.aps.connect('tcp://127.0.0.1:1234')
        hdl = self.aps.start_request('echo', 'hello')
        self.assertTrue(hdl)
