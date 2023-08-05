Typhoon is a wrapper around the [Tornado](https://www.tornadoweb.org/en/stable/) web framework. It offers the ability to attach log records with a trace id, which is used to trace individual HTTP requests. By default Typhoon obtains trace id from the request's header `X-TRACEID`. To change this behavior, subclass `typhoon.web.Application` and overwrite the `get_trace_id` method.

## Requirements
- tornado >= 5.1
  
## Installation
- Use pip:
  ```
  pip install typhoon-web
  pip install typhoon-web --upgrade
  ```
- Clone repository and install with:
  ```
  python setup.py install
  ```

## Hello, world

Here is a simple “Hello, world” example web app for Typhoon:
```python
import logging
import time

import tornado.ioloop
import typhoon.web
import typhoon.log

class MainHandler(typhoon.web.RequestHandler):
    @typhoon.web.run_in_executor
    def process(self):
        logging.info('go to sleep')
        time.sleep(3)
        logging.info('wake up')
        return 'Hello, world'

    async def get(self):
        result = await self.process()
        self.write(result)
    
    # Native coroutine (using async def and await) was introduced in Python 3.5.
    # For previous version, use generator-based coroutine. 
    # For example:
    #
    # @tornado.gen.coroutine
    # def get(self):
    #     result = yield self.process()
    #     self.write(result)

def make_app():
    return typhoon.web.Application([
        (r'/', MainHandler),
    ])

if __name__ == '__main__':
    typhoon.log.configure(log_path='/home/logs')
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```
In this example, three different log files will be generated in the log_path:
- **access.log** records summaries of each http request.
- **stats.log** records messages for statistics and analysis.
- **app.log** contains all logs that are neither access logs nor stats logs.

To log to stats.log, use an instance of `typhoon.log.StatsLogger`:
```python
import typhoon.log

stats_log = typhoon.log.StatsLogger()

stats_log.info({'user_count': 100})
stats_log.info({'job_register': 20}, topic='register')
```
Notice that logging methods of `StatsLogger` only accept a `dict` object as message.

## Trace id
By default trace id is automatically obtained and handled by Typhoon only when the client sends a request with a header `X-TRACEID: some-value`:
```bash
$ curl -H "X-TRACEID: ceon1haa6cau1dung1" http://127.0.0.1:8888
```

To customize the way trace id is passed, subclass `typhoon.web.Application` and overwrite the `get_trace_id` method.
```python
import typhoon.web

class MyApplication(typhoon.web.Application):
    def get_trace_id(self, handler):
        # obtain trace id from URL Parameter.
        return handler.get_argument('traceId', '-')
```
In the above example, trace id is passed through an URL parameter:
```bash
$ curl http://127.0.0.1:8888?traceId=ceon1haa6cau1dung1
```

You may have to call another service and pass down the trace id. In this case, use `typhoon.log.TRACE_ID()` to obtain current trace id:
```python
import requests
import typhoon.web
import typhoon.log

class MainHandler(typhoon.web.RequestHandler):
    @typhoon.web.run_in_executor
    def process(self):
        # call another service and pass down current trace id.
        r = request.get('http://127.0.0.1:9990/hello', header={'X-TRACEID': typhoon.log.TRACE_ID()})
        if r.status_code == 200:
            return 'Hello, world'
        else:
            return 'oops!'

    async def get(self):
        result = await self.process()
        self.write(result)