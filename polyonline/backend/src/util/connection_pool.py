# -*- coding:utf-8 -*- 

import logging
import MySQLdb
import threading

class MySQLConnectionPool(object):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._cached_pool = []
        self._lock = threading.Lock()
        conn = self.connect()
        conn.close()

    def connect(self):
        with self._lock:
            try:
                logging.debug('get connection from pool')
                _connect = self._cached_pool.pop(0)
            except IndexError:
                logging.debug('make connection')
                _connect = MySQLConnection(*self._args, **self._kwargs)
            else:
                _connect.reconnect()
            _pooled_connect = MySQLPooledConnection(self, _connect)
            return _pooled_connect

    def cache(self, connect):
        with self._lock:
            logging.debug('cache connection')
            self._cached_pool.append(connect)

    def close(self):
        logging.debug('close cached all connection')
        while self._cached_pool:
            _connect = self._cached_pool.pop(0)
            try:
                _connect.close()
            except Exception, e:
                logging.warning(e)

class MySQLPooledConnection(object):
    def __init__(self, connection_pool, connect):
        self._connection_pool = connection_pool
        self._connect = connect

    def close(self):
        if self._connect:
            self._connection_pool.cache(self._connect)
            self._connect = None

    def __getattr__(self, name):
        if self._connect:
            return getattr(self._connect, name)

class MySQLConnection(object):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._connect = MySQLdb.connect(*self._args, **self._kwargs)
        self._connect.set_character_set('utf8')

    def reconnect(self):
        _reconnect = False
        try:
            self._connect.ping()
        except Exception, e:
            logging.warning(e)
            logging.warning('start reconnect')
            _reconnect = True
        if _reconnect:
            try:
                _new_connect = MySQLdb.connect(*self._args, **self._kwargs)
            except Exception, e:
                logging.warning(e)
            else:
                self._connect.close()
                self._connect = _new_connect
                self._connect.set_character_set('utf8')

    def cursor(self):
        cur = self._connect.cursor()
        cur.execute('set names utf8;')
        cur.execute('set character set utf8;')
        cur.execute('set character_set_connection=utf8;')
        cur.execute('set autocommit=1;')
        return cur

    def cursor2(self):
        cur = self._connect.cursor()
        cur.execute('set names utf8;')
        cur.execute('set character set utf8;')
        cur.execute('set character_set_connection=utf8;')
        return cur

    def __enter__(self, *args, **kwargs):
        return self._connect.__enter__(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        return self._connect.__exit__(*args, **kwargs)

    def commit(self):
        self._connect.commit()

    def rollback(self):
        self._connect.rollback()

    def close(self):
        self._connect.close()

    def set_character_set(self, code_type):
        self._connect.set_character_set(code_type)


