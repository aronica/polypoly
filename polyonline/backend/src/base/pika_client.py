# -*- coding:utf-8 -*- 

import logging
import uuid
import time
import greenlet
from pika import PlainCredentials, ConnectionParameters, BasicProperties
from pika.adapters.tornado_connection import TornadoConnection
from async_client import AsyncClient
from json_serialization import json_to_class, class_to_json
from tornado import ioloop

class PikaClient(AsyncClient):

    APP_ID = 'poseidon.framework'
    EXCHANGE_TYPE_TOPIC = 'topic'
    EXCHANGE_TYPE_DIRECT = 'direct'

    def __init__(self, **kwargs):
        super(PikaClient, self).__init__(**kwargs)
        self._app_id = kwargs['app_id']
        self._mq_host_name = kwargs['host_name']
        self._mq_host_port = kwargs['host_port']
        self._mq_user = kwargs['user']
        self._mq_pwd = kwargs['pwd']
        self._mq_virtual_host = '/'
        if kwargs.has_key('ioloop'):
            self._io_loop = kwargs['ioloop']
        else:
            self._io_loop = ioloop.IOLoop.current()
        self._exchange_name = None
        self._callback_exchange_name = None
        self._connecting = False
        self._connected = False
        self._closing = False
        self._connection = None
        self._channel = None
        self._queue_name = None
        self._callback_queue_name = None
        self._routing_key = None
        self._package = None
        self._correlation_id = None
        self._custom_callback = None

    def _connect(self):
        #logging.debug('start connect to rabbitmq')
        if self._connecting:
           logging.info('PikaClient: already connecting to rabbitmq')
           return

        self._connecting = True
        credential = PlainCredentials(self._mq_user, self._mq_pwd)
        params = ConnectionParameters(
                     host = self._mq_host_name,
                     port = self._mq_host_port,
                     virtual_host = self._mq_virtual_host,
                     credentials = credential
                 )

        #logging.debug('connection params %s', params)
        self._connection = TornadoConnection(params,
                               on_open_callback = self._on_connection_open,
                               stop_ioloop_on_close = False)

    def _on_connection_open(self, connection):
        #logging.debug('connection open')
        self._connected = True
        self._connection = connection
        self._connection.WARN_ABOUT_IOLOOP = False
        self._connection.add_on_close_callback(self._on_connection_closed)
        self._on_open_channel()

    def _on_connection_closed(self, connection, reply_code, reply_text):
        self._connecting = False
        self._connected = False

    def _on_open_channel(self):
        self._connection.channel(on_open_callback = self._on_channel_opened)

    def _on_channel_opened(self, channel):
        #logging.debug('channel opened')
        self._channel = channel
        self._channel.add_on_close_callback(self._on_channel_closed)
        self._setup_exchange()

    def _on_channel_closed(self, channel, reply_code, reply_text):
        if not self._closing:
            self._connection.close()

    def _setup_exchange(self):
        self._channel.exchange_declare(self._on_exchange_declare_ok,
                                       self._callback_exchange_name,
                                       self.EXCHANGE_TYPE_DIRECT)

    def _on_exchange_declare_ok(self, frame):
        #logging.debug('exchange ready')
        self._setup_queue()

    def _setup_queue(self):
        #self._channel.queue_declare(self._on_queue_declare_ok,
        #                            queue = self._callback_queue_name,
        #                            durable = True)
        self._channel.queue_declare(self._on_queue_declare_ok,
                                             exclusive = True)

    def _on_queue_declare_ok(self, frame):
        self._callback_queue_name = frame.method.queue
        self._channel.queue_bind(self._on_bind_ok,
                                 exchange = self._callback_exchange_name,
                                 queue = self._callback_queue_name,
                                 routing_key = self._callback_queue_name)

    def _on_bind_ok(self, frame):
        self._channel.basic_consume(self._on_message_response,
                                    queue = self._callback_queue_name)
        self._publish_message()

    def _publish_message(self):
        logging.debug('publish message ...')
        properties = BasicProperties(app_id = self.APP_ID,
                                     content_type = 'text/plain',
                                     delivery_mode = 2, # make message persisdent
                                     correlation_id = self._correlation_id,
                                     reply_to = self._callback_queue_name,
                                     headers = {
                                         'callback_exchange': self._callback_exchange_name 
                                     })

        self._channel.basic_publish(exchange = self._exchange_name,
                                    routing_key = self._routing_key,
                                    body = self._package,
                                    properties = properties)

    def _on_message_response(self, channel, deliver, properties, body):
        logging.debug('on_message_response %s', body)
        if self._correlation_id != properties.correlation_id:
            logging.debug('not match correlation id')
            return
        self._acknowledge_message(deliver.delivery_tag)
        result = json_to_class(body, globals())
        if self._custom_callback:
            self._custom_callback(result)
        self._close()
        
    def _acknowledge_message(self, delivery_tag):
        self._channel.basic_ack(delivery_tag)

    def _close(self):
        self._closing = True
        self._result = None
        self._channel.close()
        self._connection.close()

    def send_call(self, module_name, package, callback):
        logging.info('send call to %s with package %s', module_name, package)
        pkg_name = package.__class__.__name__
        self._correlation_id = str(uuid.uuid4())
        self._custom_callback = callback 
        self._queue_name = module_name + '.queue'
        self._exchange_name = '%s.%s.%s' % (self._app_id, module_name, 'exchange')
        self._callback_exchange_name = '%s.%s' % (self._exchange_name, 'callback')
        self._routing_key = '%s.%s' % (module_name, pkg_name)
        self._package = class_to_json(package)
        self._io_loop.add_timeout(0, self._connect)

        
        
