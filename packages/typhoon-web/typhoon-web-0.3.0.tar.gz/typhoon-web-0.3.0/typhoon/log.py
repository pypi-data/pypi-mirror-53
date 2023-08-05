"""
typhoon.log module
"""
import logging
from logging import DEBUG, ERROR, INFO, WARNING
from contextlib import contextmanager

from .util import RecordId, TraceId

TRACE_ID = TraceId()
RECORD_ID = RecordId()


class TraceLogFormatter(logging.Formatter):
    """
    A log formatter that automatically attaches traceId and recordId to log records.
    """

    def __init__(self, fmt=None, datefmt=None, stats=False):
        super(TraceLogFormatter, self).__init__(fmt, datefmt)
        self._stats = stats

    def format(self, record):
        if not hasattr(record, 'traceId'):
            setattr(record, 'traceId', TRACE_ID())
        if self._stats:
            if not hasattr(record, 'recordId'):
                setattr(record, 'recordId', RECORD_ID())
        return super(TraceLogFormatter, self).format(record)


class StatsLogger(object):
    """
    Logger for stats log.
    """

    def __init__(self):
        self.logger = logging.getLogger('typhoon.stats')

    def setLevel(self, level):
        """
        Set the logging level of this logger.  level must be an int or a str.
        """
        self.logger.setLevel(level)

    def addHandler(self, hdlr):
        """
        Add the specified handler to this logger.
        """
        self.logger.addHandler(hdlr)

    def removeHandler(self, hdlr):
        """
        Remove the specified handler from this logger.
        """
        self.logger.removeHandler(hdlr)

    def debug(self, msg, topic='default'):
        """
        Log 'msg' with severity 'DEBUG'.

        Parameters
        ----------
        msg : dict
            message to log
        topic : str, optional
            topic, by default 'default'
        """
        self._log(DEBUG, msg, topic)

    def info(self, msg, topic='default'):
        """
        Log 'msg' with severity 'INFO'.

        Parameters
        ----------
        msg : dict
            message to log
        topic : str, optional
            topic, by default 'default'
        """
        self._log(INFO, msg, topic)

    def warning(self, msg, topic='default'):
        """
        Log 'msg' with severity 'WARNING'.

        Parameters
        ----------
        msg : dict
            message to log
        topic : str, optional
            topic, by default 'default'
        """
        self._log(WARNING, msg, topic)

    def error(self, msg, topic='default'):
        """
        Log 'msg' with severity 'ERROR'.

        Parameters
        ----------
        msg : dict
            message to log
        topic : str, optional
            topic, by default 'default'
        """
        self._log(ERROR, msg, topic)

    def _log(self, level, msg, topic):
        if not isinstance(msg, dict):
            raise TypeError('msg of stats logger must be a dict')

        if not isinstance(level, int):
            raise TypeError('level must be an integer')

        extra = {'topic': topic}
        if self.logger.isEnabledFor(level):
            fn, lno, func, sinfo = self.logger.findCaller(False)
            record = self.logger.makeRecord(self.logger.name, level, fn, lno, msg, args=None, exc_info=False, extra=extra, func=func, sinfo=sinfo)
            self.logger.handle(record)


@contextmanager
def trace(trace_id):
    """
    A contex manager.

    Use it like:

    with trace(trace_id='123'):
        do_something()

    The trace id will be stored in a ThreadLocal variable before the execution of `do_something()`
    and deleted after the execution.
    In this way, `.TraceLogFormatter` could obtain the trace id during the execution of `do_something()`.

    Parameters
    ----------
    trace_id : str
        trace id.
    """
    TRACE_ID.set_trace(trace_id)
    try:
        yield
    finally:
        TRACE_ID.del_trace()


def configure(log_path, access=True, stats=True, app=True, level='info', suffix=None, backup_count=90):
    """
    Configure loggers.

    Parameters
    ----------
    log_path : str
        path to place log files.
    access : bool, optional
        whether to generate access.log, by default True
    stats : bool, optional
        whether to generate stats.log, by default True
    app : bool, optional
        whether to generate app.log, by default True
    level : str, optional
        log level, by default 'info'
    suffix : str, optional
        suffix of log files, by default None
    backupCount : int, optional
        count of backup files, by default 90
    """
    if not any((access, stats, app)):
        return

    import os

    logging._handlers.clear()
    logging.shutdown(logging._handlerList[:])
    del logging._handlerList[:]

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper()))

    access_log = logging.getLogger('tornado.access')
    stats_log = logging.getLogger('typhoon.stats')

    if suffix is None:
        file_suffix = 'log'
    else:
        file_suffix = 'log.%s' % suffix

    if access:
        access_fmt = logging.Formatter(
            fmt='[%(asctime)s][%(traceId)s][%(levelname)s][%(process)d]%(message)s',
            datefmt='%d/%b/%Y:%H:%M:%S %z'
        )
        access_hdlr = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_path, 'access.%s' % file_suffix),
            when='midnight',
            backupCount=backup_count,
            encoding='utf-8'
        )
        access_hdlr.setFormatter(access_fmt)
        access_log.addHandler(access_hdlr)
        access_log.propagate = False

    if stats:
        stats_fmt = TraceLogFormatter(
            fmt='time=%(asctime)s.%(msecs)d, traceId=%(traceId)s, module=%(module)s, topic=%(topic)s, id=%(recordId)s, message=%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            stats=True
        )
        stats_hdlr = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_path, 'stats.%s' % file_suffix),
            when='midnight',
            backupCount=backup_count,
            encoding='utf-8'
        )
        stats_hdlr.setFormatter(stats_fmt)
        stats_log.addHandler(stats_hdlr)
        stats_log.propagate = False

    if app:
        access_log.propagate = False
        stats_log.propagate = False

        app_fmt = TraceLogFormatter(
            fmt='{time=%(asctime)s.%(msecs)d, traceId=%(traceId)s, level=%(levelname)s, pid=%(process)d, module=%(module)s, func=%(funcName)s, line=%(lineno)d}%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        app_hdlr = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_path, 'app.%s' % file_suffix),
            when='midnight',
            backupCount=backup_count,
            encoding='utf-8'
        )
        app_hdlr.setFormatter(app_fmt)
        root.addHandler(app_hdlr)
