# -*- coding:utf-8 -*-

import traceback
import logging
import time
from base.redis_server import RedisServer
import base.module as module
from base.redis_manager import RedisRegisterManager
from functools import wraps, partial
import greenlet
from base.redis_client import RedisClient
from tornado import web, ioloop

def async_method(func):
    @wraps(func)
    def wrapper(self, *kargs, **kwargs):
        def greenlet_func():
            func(self, *kargs, **kwargs)
        gr = greenlet.greenlet(greenlet_func)
        gr.switch()
    return wrapper

class AsyncService(RedisServer):
    def __init__(self, module_name,  **kwargs):
        kwargs['module_name'] = module_name
        self._module_name = module_name
        server_config = kwargs['server_redis']
        register_config = kwargs['register_redis']
        #RedisRegisterManager.register_service(register_config['host'], register_config['port'], module_name, server_config['host'], server_config['port'])
        RedisRegisterManager.get_register_services(register_config['host'], register_config['port'])
        assert RedisRegisterManager.SERVICE_DICT.has_key(module_name)
        super(AsyncService, self).__init__(**kwargs)

    def send_call(self, module_name, package, timeout = 10):
        def __on_callback(result):
            self.io_loop.add_callback(partial(gr.switch, result))
        try:
            gr = greenlet.getcurrent()
            host, port = RedisRegisterManager.get_service_config(module_name)
            client = RedisClient(self._module_name, host, port, self.io_loop)
            client.send_call(module_name, package, __on_callback, timeout)
            result = gr.parent.switch()
            return result
        except Exception, e:
            logging.error(e, exc_info=True)
            return None

    def send_message(self, module_name, package):
        try:
            host, port = RedisRegisterManager.get_service_config(module_name)
            client = RedisClient(self._module_name, host, port, self.io_loop)
            client.send_message(module_name, package)
        except Exception, e:
            logging.debug(e, exc_info=True)


