# -*- coding:utf-8 -*-

import logging
import json
import signal
import requests
import base.module as module
import util.connection_pool as connection_pool
from base.async_server import AsyncService, async_method
from base.messages import *
from datetime import datetime

class WeixinService(AsyncService):
    def __init__(self, **kwargs):
        super(WeixinService, self).__init__(module.MODULE_WEIXIN, **kwargs)
        mysql_config = kwargs["mysql"]
        self.conn_pool = connection_pool.MySQLConnectionPool(host = mysql_config['host'], user = mysql_config['user'], passwd = mysql_config['pwd'], db = mysql_config['db'])

    def on_call_WeixinUserInfo(self, pkg):
        if pkg.action == pkg.SET:
            return self.set_information(pkg)
        elif pkg.action == pkg.GET:
            return self.get_information(pkg)
        else:
            assert False


    def set_information(self, pkg):
        res = PostResponse()
        res.status = res.FAIL
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        try:
            sql = "insert into weixin_profile (openid, unionid, nickname, sex, headimgurl, country, province, city, lang) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update nickname = %s, sex = %s, headimgurl = %s, country = %s, province = %s, city = %s, lang = %s, last_login = %s"
            params = [pkg.openid, pkg.unionid, pkg.nickname, pkg.sex, pkg.headimgurl, pkg.country, pkg.province, pkg.city, pkg.lang, pkg.nickname, pkg.sex, pkg.headimgurl, pkg.country, pkg.province, pkg.city, pkg.lang, datetime.now()]
            cursor.execute(sql, params)
            res.status = res.SUCCESS
        except Exception as e:
            logging.error(e, exc_info = True)
        conn.close()
        return res

    def get_information(self, pkg):
        res = WeixinUserInfo()
        res.status = res.FAIL
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        sql = "select nickname, headimgurl from weixin_profile where openid = %s limit 1"
        params = [pkg.openid]
        try:
            cursor.execute(sql, params)
        except Exception as e:
            logging.error(e, exc_info = True)
            return res
        if cursor.rowcount == 0:
            res.status = res.NO_USER
            return res
        res.nickname, res.headimgurl = cursor.fetchone()
        res.openid = pkg.openid
        res.status = res.SUCCESS
        conn.close()
        return res

def start_server(config):
    server_config = config['server_redis']
    register_config = config['register_redis']
    mysql_db = config['mysql']
    service = WeixinService(**config)
    service.server_config = server_config
    service.register_config = register_config
    service.module_configs = {}
    signal.signal(signal.SIGTERM, service.stop)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    service.run()

