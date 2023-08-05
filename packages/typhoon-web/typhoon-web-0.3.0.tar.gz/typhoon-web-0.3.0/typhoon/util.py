"""
typhoon.util module
"""
import hashlib
import socket
import sys
import time
import threading


def _get_host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class RecordId(object):
    """
    Record id generator.
    """

    def __init__(self):
        self.host = _get_host()
        self.count = 0
        self.main_path = sys.argv[0]

    def __call__(self):
        self.count += 1
        hl = hashlib.md5()
        string = self.host + self.main_path + str(time.time()) + str(id(hl)) + str(self.count)
        hl.update(string.encode(encoding='utf-8'))
        return hl.hexdigest()


class TraceId(threading.local):
    """
    Trace id manager.
    """

    def __call__(self):
        return getattr(self, 'traceId', '-')

    def set_trace(self, trace_id):
        setattr(self, 'traceId', trace_id)

    def del_trace(self):
        delattr(self, 'traceId')
