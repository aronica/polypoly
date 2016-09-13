# -*- coding:utf-8 -*- 
import logging

class AsyncBase(object):
    
    PUBLISH_INTERVAL = 1
    EXCHANGE_TYPE_TOPIC = 'topic'
    EXCHANGE_TYPE_DIRECT = 'direct'

    def __init__(self):
        pass


