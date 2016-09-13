# -*- coding:utf-8 -*- 

import logging
import uuid
import time
from tornado.ioloop import IOLoop
from functools import partial, wraps
import greenlet
from json_serialization import json_to_class, class_to_json
import redis
from base.redis_manager import RedisConnectionPoolManager 

def async_method(func):
    @wraps(func)
    def wrapper(self, *kargs, **kwargs):
        def greenlet_func():
            func(self, *kargs, **kwargs)
        gr = greenlet.greenlet(greenlet_func)
        gr.switch()
    return wrapper

class RedisServer(object):
    def __init__(self, **kwargs):
        self._module_name = kwargs['module_name']
        self._register_redis_config = kwargs['register_redis']
        self._server_redis_config  = kwargs['server_redis']
        self.io_loop = IOLoop.instance()

    def _on_message_arriave(self):
        @async_method
        def __on_call(self, package):
            list_name = '%s.callback.%s' % (package._base_msg_info.send_service_name, package._base_msg_info.message_id)
            def __send_callback(self, result):
                self._redis.lpush(list_name, class_to_json(result))
            method_name = 'on_call_' + package_name
            if hasattr(self, method_name):
                result = getattr(self, method_name)(package)
                __send_callback(self, result)
            else:
                logging.error('cannot find method %s' % method_name)

        def __on_message(self, package):
            method_name = 'on_message_' + package_name
            if hasattr(self, method_name):
                result = getattr(self, method_name)(package)
        try:
            result = self._redis.brpop(self._module_name, timeout=1)
            if result is not None:
                if len(result) != 2:
                    raise
                package = json_to_class(result[1])
                package_name = package.__class__.__name__
                msg_info = package._base_msg_info
                if msg_info.send_type == msg_info.SEND_CALL:
                    on_call = partial(__on_call, self, package)
                    self.io_loop.add_timeout(time.time(), on_call)
                elif msg_info.send_type == msg_info.SEND_MESSAGE:
                    on_message = partial(__on_message, self, package)
                    self.io_loop.add_timeout(time.time(), on_message)
        except Exception, e:
            logging.error(e, exc_info=True)
        self.io_loop.add_timeout(time.time(), self._on_message_arriave)

    def run(self):
        host = self._server_redis_config['host']
        port = self._server_redis_config['port']
        self._redis_pool = RedisConnectionPoolManager.get_pool(host, port)

        self._redis = redis.StrictRedis(connection_pool = self._redis_pool)
        self.io_loop.add_timeout(time.time(), self._on_message_arriave)
        self.io_loop.start()

    def stop(self, signum, frame):
        if self.io_loop is not None:
            self.io_loop.stop()
        
