# -*- coding:utf-8 -*- 

import logging
import redis

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class RedisConnectionPoolManager(object):
    __metaclass__ = Singleton
    CONNECTION_DICT = {} 
    
    @staticmethod
    def get_pool(host, port):
        key = '%s.%s' % (host, port)
        if RedisConnectionPoolManager.CONNECTION_DICT.has_key(key):
            return RedisConnectionPoolManager.CONNECTION_DICT[key]
        else:
            pool = redis.ConnectionPool(host = host, port = port, db = 0)
            RedisConnectionPoolManager.CONNECTION_DICT[key] = pool
            return pool


class RedisRegisterManager(object):

    SERVICE_DICT = {}
  
    @staticmethod
    def get_service_config(module_name):
        if RedisRegisterManager.SERVICE_DICT.has_key(module_name):
            value = RedisRegisterManager.SERVICE_DICT[module_name]
            return value.split(':')
        else:
            raise Exception('cannot find %s redis config' % module_name)

    @staticmethod
    def get_register_services(register_host, register_port):
        pool = RedisConnectionPoolManager.get_pool(register_host, register_port)
        r = redis.StrictRedis(connection_pool = pool)
        RedisRegisterManager.SERVICE_DICT =  r.hgetall('service_dict')

    @staticmethod
    def register_service(register_host, register_port, module_name, service_host, service_port):
        logging.info("please run script to register all service in advance")
        assert False
        pool = RedisConnectionPoolManager.get_pool(register_host, register_port)
        r = redis.StrictRedis(connection_pool = pool)
        r.hset('service_dict', module_name, '%s:%s' % (service_host, service_port))


        

        
