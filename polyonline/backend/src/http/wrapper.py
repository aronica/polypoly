# -*- coding:utf-8 -*-

import logging
import traceback
from base.tornado_client import TornadoRequestHandler, greenlet_wrapper
import public_var
import base.module as module
from tornado.ioloop import IOLoop
import gzip
import cStringIO
import json

def check_url_parameter(parameters):
    def wrapper(method):
        def check_parameter(self):
            for param in parameters:
                value = self.get_argument(param, None)
                if value is None:
                    self.make_return(public_var.RESULT_CODE_CLIENT_ERROR, 'missing parameter %s' % param, '')
                    return False
            return True

        def _wrapper(self, *args, **kwargs):
            if check_parameter(self):
                method(self, *args, **kwargs)
        return _wrapper
    return wrapper

def check_body_parameter(parameters):
    def wrapper(method):
        def check_parameter(self):
            self.body = self.load_body()
            for param in parameters:
                if not self.body.has_key(param):
                    self.make_return(public_var.RESULT_CODE_CLIENT_ERROR, 'missing parameter %s' % param, '')
                    return False
            return True
        def _wrapper(self, *args, **kwargs):
           if check_parameter(self):
                method(self, *args, **kwargs)
        return _wrapper
    return wrapper

class BaseHandler(TornadoRequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def load_body(self):
        try:
            try:
                data = json.loads(self.request.body, encoding='utf-8')
            except:
                f = gzip.GzipFile(mode = 'rb', fileobj = cStringIO.StringIO(self.request.body))
                data = json.loads(f.read(), encoding='utf-8')
            return data
        except Exception, e:
            logging.debug(e, exc_info=True)
            return None

    def check_body_parameters(self, body, params):
        for param in params:
            if not body.has_key(param):
                self.make_return(public_var.RESULT_CODE_CLIENT_ERROR, 'missing parameter %s' % param, '')
                return False
        return True

    def make_return(self, result_code, result_msg, result):
        body = {
            'resultCode': result_code,
            'resultStatus': result_msg,
            'result': result
        }
        logging.debug(json.dumps(body, encoding='utf-8'))
        self.write(json.dumps(body, encoding='utf-8'))





