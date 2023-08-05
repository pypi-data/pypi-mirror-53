"""
typhoon.web module
"""
import tornado.web
from tornado.log import access_log, app_log, gen_log

from .coroutine import run_in_executor


class Application(tornado.web.Application):
    """
    A subclass of `tornado.web.Application`.

    The `log_request` method is overwritten so that the trace id is obtained
    and attached to the access log.
    """

    def log_request(self, handler):
        trace_id = self.get_trace_id(handler)
        extra = {'traceId': trace_id}

        if "log_function" in self.settings:
            self.settings["log_function"](handler)
            return
        if handler.get_status() < 400:
            log_method = access_log.info
        elif handler.get_status() < 500:
            log_method = access_log.warning
        else:
            log_method = access_log.error
        request_time = 1000.0 * handler.request.request_time()
        log_method(
            "%d %s %.2fms",
            handler.get_status(),
            handler._request_summary(),
            request_time,
            extra=extra
        )

    def get_trace_id(self, handler: tornado.web.RequestHandler) -> str:
        """
        Get trace id from a specified request.

        By default trace id is extracted from the request's head `X-TRACEID`.
        To change this behavior, subclass Application and override this method.
        """
        if hasattr(handler, '__trace_id'):
            trace_id = getattr(handler, '__trace_id')
        else:
            trace_id = handler.request.headers.get('X-TRACEID', '-')
            setattr(handler, '__trace_id', trace_id)
        return trace_id


class RequestHandler(tornado.web.RequestHandler):
    """
    A subclass of `tornado.web.RequestHandler`.

    The `log_exception` method is overwritten so that the trace id is obtained
    and attached to the exception log.
    """

    def log_exception(self, typ, value, tb):
        trace_id = self.application.get_trace_id(self)
        extra = {'traceId': trace_id}

        if isinstance(value, tornado.web.HTTPError):
            if value.log_message:
                format = "%d %s: " + value.log_message
                args = [value.status_code, self._request_summary()] + list(value.args)
                gen_log.warning(
                    format,
                    *args,
                    extra=extra
                )
        else:
            app_log.error(
                "Uncaught exception %s\n%r",
                self._request_summary(),
                self.request,
                exc_info=(typ, value, tb),
                extra=extra
            )
