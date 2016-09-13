#!/usr/bin/env python
#coding:utf8

import http.wrapper as wrapper
import base.messages as message
import base.module as module
import json
import logging
import public_var
from base.tornado_client import greenlet_wrapper

class GetIndexDataHandler(wrapper.BaseHandler):
    @greenlet_wrapper
    def get(self):
        self.do()

    def do(self):
        req = message.OperateRequest()
        req.action = req.GET_INDEX
        res = self.send_call(module.MODULE_OPERATE, req)
        if res.status == res.SUCCESS:
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', res.result)
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)

