# -*- coding:utf-8 -*-

import logging
import json
import signal
import base.module as module
import util.connection_pool as connection_pool
from base.async_server import AsyncService, async_method
from base.messages import *
from datetime import datetime

class OperateService(AsyncService):
    def __init__(self, **kwargs):
        super(OperateService, self).__init__(module.MODULE_OPERATE, **kwargs)
        mysql_config = kwargs["mysql"]
        self.conn_pool = connection_pool.MySQLConnectionPool(host = mysql_config['host'], user = mysql_config['user'], passwd = mysql_config['pwd'], db = mysql_config['db'])
        self.index = kwargs["index"]

    def on_call_OperateRequest(self, pkg):
        if pkg.action == pkg.GET_INDEX:
            return self.get_index_data()

    def get_index_data(self):
        res = OperateResponse()
        res.status = res.SUCCESS
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        result = {}
        now = datetime.now()
        for key in self.index:
            result[key] = []
            for item in self.index[key]:
                is_valid = True
                if item["datetime_from"] and datetime.strptime(item["datetime_from"], "%Y%m%d%H%M%S") > now:
                    is_valid = False
                elif item["datetime_to"] and datetime.strptime(item["datetime_to"], "%Y%m%d%H%M%S") < now:
                    is_valid = False
                if is_valid:
                    d = {}
                    d["image"] = item["image"]
                    d["type"] = item["type"]
                    if item["type"] == "structure":
                        sql = "select id from structure where name = %s limit 1"
                        params = [item["name"]]
                        cursor.execute(sql, params)
                        if cursor.rowcount == 1:
                            structure_id = cursor.fetchone()[0]
                            d["structure_id"] = structure_id
                            result[key].append(d)
                    else:
                        d["link"] = item["link"]
                        result[key].append(d)
        conn.close()
        res.result = result
        return res


def start_server(config):
    server_config = config['server_redis']
    register_config = config['register_redis']
    mysql_db = config['mysql']
    service = OperateService(**config)
    service.server_config = server_config
    service.register_config = register_config
    service.module_configs = {}
    signal.signal(signal.SIGTERM, service.stop)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    service.run()

