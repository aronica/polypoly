# -*- coding:utf-8 -*- 

import logging
import start_base
import comment.service as COMMENT
import base.module as module

class App(start_base.Daemon):
    def __init__(self, module_name):
        super(App, self).__init__(module_name)

    def real_run(self, hid, config):
        COMMENT.start_server(config)

if __name__ == '__main__':
    start_base.run_server(App(module.MODULE_COMMENT), 'comment')

