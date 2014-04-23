# -*- coding: utf-8 -*-
import zmq

from aps.base import aps_send_frames, aps_recv_frames, default_timeout,\
    register_socket, pending_requests
from aps.message import APSRequest
from aps.util import get_timestamp, get_uuid



class APS(object):
    """APS Client class
    """

    seq = 0

    def __init__(self):
        self._ctx = zmq.Context()
        self.poller = zmq.Poller()
        self.sockets = set()

    def connect(self, endpoint):
        """connect to an APS endpoint

        Args:
            +endpoint+ an APS format like zmq endpoint

        Returns:
            +sock+ an zmq socket
        """
        _sock = self._ctx.socket(zmq.DEALER)
        _sock.setsockopt(zmq.LINGER, 0)
        _sock.connect(endpoint)
        register_socket(_sock)
        self._sock = _sock
        return _sock

    def start_request(self, method, params=[], callback=None, expiry=0,
                      extras=None):
        """send an APS request to corespanding endpoint

        Args:
            +method+ the method namel see APS spec
            +*params+ the parameter list, in order
            +callback+ register a callback when ready
        """
        request = APSRequest(method=method, params=params,
                             sequence=APS.next_seq(),
                             expiry=expiry, extras=extras)
        pending_requests[request.sequence] = (request, callback)
        aps_send_frames(self._sock, request.frames)
        return request.sequence

    @staticmethod
    def next_seq():
        APS.seq += 1
        return APS.seq
