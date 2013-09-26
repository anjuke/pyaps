from unittest import TestCase
from datetime import datetime
from aps.base import get_timestamp

class APSTestCase(TestCase):

    def setUp(self):

        pass

    def tearDown(self):
        pass


    def test_get_timestamp(self):
        ts = get_timestamp()
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

    #TODO: send_frames / recv_frames test, threading ?
