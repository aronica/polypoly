# -*- coding:utf-8 -*- 

import logging
import uuid
import time
from pika import PlainCredentials, ConnectionParameters, BasicProperties
from pika.adapters.select_connection import SelectConnection
from pika.adapters.tornado_connection import TornadoConnection
from json_serialization import json_to_class, class_to_json
from tornado import ioloop

class PikaBase(object):
    def __init__(self, host_name, host_port, user, pwd, virtual_host, exchange_name, exchange_type, queue_name = None, routing_key = None, tornado_io_loop = None):
        self._mq_host_name = host_name
        self._mq_host_port = host_port
        self._mq_user = user
        self._mq_pwd = pwd
        self._mq_virtual_host = virtual_host
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._queue_name = queue_name
        self._routing_key = None
        if routing_key is not None:
            self._routing_key = routing_key
        self._io_loop = None
        if tornado_io_loop is not None:
            self._io_loop = tornado_io_loop
        self._connecting = False
        self._connected = False
        self._closing = False
        self._connection = None
        self._channel = None
        self._server_tag = None

    def _connect(self):
        if self._connecting:
            logging.info('Pika: already connecting to rabbitmq')
            return

        logging.debug('Pika: connectiong to rabbitmq')
        self._connecting = True
        credential = PlainCredentials(self._mq_user, self._mq_pwd)
        params = ConnectionParameters(
                    host = self._mq_host_name,
                    port = self._mq_host_port,
                    virtual_host = self._mq_virtual_host,
                    credentials = credential)
        if self._io_loop is None:
            self._connection = SelectConnection(params,
                                   on_open_callback = self._on_connection_open,
                                   stop_ioloop_on_close = False)
        else:
            self._connection = TornadoConnection(params,
                                   on_open_callback = self._on_connection_open)
    
    def _on_connection_open(self, connection):
        logging.debug('Pika: connected to rabbitmq')
        self._connected = True
        self._connection = connection
        self._connection.add_on_close_callback(self._on_connection_closed)
        self._on_open_channle()

    def _on_connection_closed(self, connection, reply_code, reply_text):
        logging.debug('Pika: connection was closed (%s) %s', reply_code, reply_text)
        self._channel = None
        self._connecting = False
        self._connected = False
        if self._closing:
            self._stop_io_loop()
        else:
            logging.debug('Pika: connection closed. reopen in 1 second')
            self._connection.add_timeout(1, self._reconneted)
        
    def _reconneted(self):
        if self._io_loop is None:
            self._connection.ioloop.stop()
            if not self._closing:
                self._connect()
                self._connection.ioloop.start()
        else:
            self._io_loop.add_timeout(1, self._connect)


    def _stop_io_loop(self):
        if self._io_loop is None:
            if self._connection is not None:
                self._connection.ioloop.stop()
        else:
            pass

    def _on_open_channle(self):
        self._connection.channel(on_open_callback = self._on_channel_opend)

    def _on_channel_opend(self, channel):
        self._channel = channel
        self._channel.add_on_close_callback(self._on_channel_closed)
        self._setup_exchange()

    def _on_channel_closed(self, channel, reply_code, reply_text):
        logging.debug('Pika: channel was closed (%s)%s', reply_code, reply_text)
        if not self._closing:
            self._connection.close()

    def _setup_exchange(self):
        self._channel.exchange_declare(self._on_exchange_declare_ok,
                                       self._exchange_name,
                                       self._exchange_type)

    def _on_exchange_declare_ok(self, frame):
        self._setup_queue()

    def _setup_queue(self):
        self._channel.queue_declare(self._on_queue_declare_ok,
                                    queue = self._queue_name,
                                    durable = True)

    def _on_queue_declare_ok(self, frame):
        self._channel.queue_bind(self._on_bind_ok, 
                                 exchange = self._exchange_name,
                                 queue = self._queue_name,
                                 routing_key = self._routing_key)

    def _on_bind_ok(self, frame):
        self._server_tag = self._channel.basic_consume(self._on_message_arrive,
                                    queue = self._queue_name)
        self._channel.basic_qos(prefetch_count = 1)
        if hasattr(self, '_on_service_ready'):
            service_ready = getattr(self, '_on_service_ready')
            self._connection.ioloop.add_timeout(0, service_ready)

    def _on_message_arrive(self, channle, deliver, properties, body):
        logging.debug('Pika: on message arrive: %s, %s, %s', deliver, properties, body)
        if hasattr(self, '_on_message_hub'):
            try:
                getattr(self, '_on_message_hub')(properties, body)
            except Exception, e:
                logging.info(e, exc_info = True)
        self._acknowledge_message(deliver.delivery_tag)

    def _acknowledge_message(self, delivery_tag):
        self._channel.basic_ack(delivery_tag)

