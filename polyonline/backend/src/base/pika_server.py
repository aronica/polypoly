# -*- coding:utf-8 -*- 

import logging
import uuid
import time
from pika import PlainCredentials, ConnectionParameters, BasicProperties
from pika.adapters.tornado_connection import TornadoConnection
from json_serialization import json_to_class, class_to_json
from pika_base import PikaBase
from tornado import ioloop

class PikaServer(PikaBase):

    EXCHANGE_TYPE_TOPIC = 'topic'
    EXCHANGE_TYPE_DIRECT = 'direct'

    def __init__(self, **kwargs):
        self._app_id = kwargs['app_id']
        self._module_name = kwargs['module_name']
        exchange_name = '%s.%s.%s' % (self._app_id, self._module_name, 'exchange')
        queue_name = self._module_name + '.queue'
        routing_key = self._module_name + '.#'
        super(PikaServer, self).__init__(kwargs['host_name'], kwargs['host_port'], kwargs['user'], kwargs['pwd'], '/', exchange_name, self.EXCHANGE_TYPE_TOPIC, queue_name, routing_key, ioloop.IOLoop.instance())

    def _on_service_ready(self):
        self._register_service()

    def _on_message_hub(self, properties, body):
        def __on_call(self, package):
            method_name = 'on_call_' + package.__class__.__name__
            if hasattr(self, method_name):
                result = getattr(self, method_name)(package)
                callback_package = class_to_json(result)
                callback_exchange = properties.headers['callback_exchange']
                callback_properties = BasicProperties(content_type = 'text/plain',
                                           correlation_id = properties.correlation_id)
                self._channel.basic_publish(exchange = callback_exchange,
                                  routing_key = properties.reply_to,
                                  properties = callback_properties,
                                  body = callback_package)
        def __on_message(self, package):
            method_name = 'on_message_' + package.__class__.__name__
            if hasattr(self, module_name):
                getattr(self, method_name)(package)
        package = json_to_class(body)
        package_name = package.__class__.__name__
        if properties.reply_to is not None:
            __on_call(self, package)
        else:
            __on_message(self, package)

    def run(self):
        self._io_loop.add_timeout(0, self._connect)
        self._io_loop.start()

    def stop(self):
        logging.info('stop pika server')
        self._closing = True
        if self._channel:
            logging.info('sending  cancel RPC command to rabbitmq')
            self._channel.basic_cancel(self._on_cancel_ok, self._server_tag)
        self._io_loop.stop()
        logging.info('pika server stopped')

    def _on_cancel_ok(self, frame):
        logging.info('closing channle')
        self._channel.close()

        




