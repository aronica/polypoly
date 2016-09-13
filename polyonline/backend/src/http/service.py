# -*- coding:utf-8 -*-

import logging
import poly
import comment
import visitor
import operate
from tornado import web, ioloop, autoreload
from base.redis_manager import RedisRegisterManager
import time

def start_server(hid, config):
    global app
    global io_loop
    settings = {
    }
    register_config = config['register_redis']
    RedisRegisterManager.get_register_services(register_config['host'], register_config['port'])
    app = web.Application([
        (r'/city/list', poly.CityListHandler),
        (r'/property/list', poly.PropertyListHandler),
        (r'/structure/filter', poly.StructureFilterHandler),
        (r'/structure/list', poly.StructureListHandler),
        (r'/structure/detail', poly.StructureDetailHandler),
        (r'/structure/export', poly.ExportHandler),
        (r'/comment', comment.StructureCommentHandler),
        (r'/comment/export', comment.ExportHandler),
        (r'/user/info/set', visitor.InformationSetHandler),
        (r'/user/weixin/set', visitor.WeixinInfoSetHandler),
        (r'/user/weixin/get', visitor.WeixinInfoGetHandler),
        (r'/user/structure/get', visitor.StructureGetHandler),
        (r'/user/export', visitor.ExportHandler),
        (r'/index', operate.GetIndexDataHandler),
    ], **settings)
    app.listen(config["start_threads"][hid])

    io_loop = ioloop.IOLoop.instance()
    io_loop.start()

def stop_server(signum, frame):
    global io_loop
    io_loop.stop()

if __name__ == '__main__':
    pass
