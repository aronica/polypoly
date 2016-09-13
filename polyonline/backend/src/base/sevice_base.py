# -*- coding:utf-8 -*- 

from base.pika_server import PikaServer

class BaseService(PikaServer):
    def __init__(self, module_name,  **kwargs):
        kwargs['queue_name'] = module_name 
        super(ProbeService, self).__init__(**kwargs)
