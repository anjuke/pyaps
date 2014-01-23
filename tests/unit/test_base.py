# -*- coding: utf-8 -*-
from unittest import TestCase



class APSTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_aps_send_frames(self):
        from aps.base import aps_send_frames
        self.assertTrue(callable(aps_send_frames))

    def test_aps_recv_frames(self):
        from aps.base import aps_recv_frames
        self.assertTrue(callable(aps_recv_frames))
