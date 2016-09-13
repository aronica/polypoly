# -*- coding:utf-8 -*- 

import logging
import uuid
import time
from tornado.ioloop import IOLoop
import redis
from json_serialization import json_to_class, class_to_json
from functools import partial
from base.redis_manager import RedisConnectionPoolManager
import greenlet

class RedisClient(object):
    def __init__(self, service_name, redis_host, redis_port, io_loop):
        self._service_name = service_name 
        self._io_loop = io_loop
        self._redis_pool = RedisConnectionPoolManager.get_pool(redis_host, redis_port)
        self._redis = redis.StrictRedis(connection_pool = self._redis_pool)
        self._retry = 0
        self._timeout = False
        self._success_callback = False

    def send_call(self, module_name, package, custom_callback, timeout_interval = 10):
        def _timeout_callback(self):
            self._timeout = True
            if not self._success_callback:
                logging.debug('callback timeout')
                custom_callback(None)
        def _callback(self, msg_id, timeout):
            if self._timeout:
                return
            list_name = '%s.callback.%s' % (self._service_name, msg_id)
            result = self._redis.brpop(list_name, timeout=10)
            if result is None:
                self._io_loop.add_timeout(time.time(), callback)
            elif not self._timeout:
                self._success_callback = True
                message = json_to_class(result[1])
                custom_callback(message)
            else:
                logging.debug('callback arriave after timeout')
        package._base_msg_info.send_service_name = self._service_name
        self._redis.lpush(module_name, class_to_json(package))
        callback =  partial(_callback, self, package._base_msg_info.message_id, timeout_interval)
        self._io_loop.add_timeout(time.time(), callback)
        timeout_callback = partial(_timeout_callback, self)
        self._io_loop.add_timeout(time.time() + timeout_interval, timeout_callback)
        
    def send_message(self, module_name, package):        
        package._base_msg_info.send_service_name = self._service_name
        package._base_msg_info.send_type = package._base_msg_info.SEND_MESSAGE
        self._redis.lpush(module_name, class_to_json(package))
 

