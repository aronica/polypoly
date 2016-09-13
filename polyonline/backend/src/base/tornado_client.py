# -*- coding:utf-8 -*- 

from tornado import web, ioloop
import logging
import json
import time
import datetime
import traceback
import uuid
import event
import greenlet
from functools import wraps, partial
from base.redis_client import RedisClient
import base.module as module
from tornado.ioloop import IOLoop
from base.redis_manager import RedisRegisterManager

def greenlet_wrapper(method):
    @web.asynchronous
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        def greenlet_base_func():
            method(self, *args, **kwargs)
            if not self._finished:
                self.finish()

        gr = greenlet.greenlet(greenlet_base_func)
        gr.switch()
        end_time = time.time()
        cost_time = end_time - start_time
        cost_time = cost_time * 1000
        url = '%s %s %s %dms' % (self.request.remote_ip, self.request.method, self.request.uri, cost_time)
        logging.info(url)
    return wrapper 

class TornadoRequestHandler(web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(TornadoRequestHandler, self).__init__(application, request, **kwargs)

    def send_call(self, module_name, package):
        def _on_callback(result):
            ioloop.IOLoop.instance().add_callback(partial(gr.switch, result)) 
        try:
            gr = greenlet.getcurrent()
            host, port = RedisRegisterManager.get_service_config(module_name)
            client = RedisClient(module.MODULE_HTTP, host, port, IOLoop.instance())
            client.send_call(module_name, package, _on_callback)
            result = gr.parent.switch() 
            return result
        except Exception, e:
            logging.error(e, exc_info=True)
            return None

    def send_message(self, module_name, package):
        try:
            host, port = RedisRegisterManager.get_service_config(module_name)
            client = RedisClient(module.MODULE_HTTP, host, port, IOLoop.instance())
            client.send_message(module_name, package)
        except Exception, e:
            logging.error(e, exc_info=True)
