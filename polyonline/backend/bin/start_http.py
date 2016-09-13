# -*- coding:utf-8 -*- 

import logging
import time
import os
import sys
import start_base
import signal
import http.service as HTTP

class App(start_base.Daemon):
    def __init__(self, module_name):
        super(App, self).__init__(module_name)

    def real_run(self, hid, config):
        signal.signal(signal.SIGTERM, HTTP.stop_server)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        HTTP.start_server(hid, config)

if __name__ == '__main__':
    start_base.run_server(App('http'), 'http')

