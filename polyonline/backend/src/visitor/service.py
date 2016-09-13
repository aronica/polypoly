# -*- coding:utf-8 -*- 

import logging
import json
import signal
import base.module as module
import util.connection_pool as connection_pool
from base.async_server import AsyncService, async_method
from base.messages import * 

class UserService(AsyncService):
    def __init__(self, **kwargs):
        super(UserService, self).__init__(module.MODULE_VISITOR, **kwargs)
        mysql_config = kwargs["mysql"]
        self.conn_pool = connection_pool.MySQLConnectionPool(host = mysql_config['host'], user = mysql_config['user'], passwd = mysql_config['pwd'], db = mysql_config['db'])

    def on_call_UserInformationRequest(self, pkg):
        if pkg.action == pkg.UPDATE:
            return self.update_information(pkg.information)
                
    def update_information(self, information):
        res = PostResponse()
        update_map = {
                "phone":information.phone,
                "family_structure":information.family_structure,
                "income_lower":information.income_lower,
                "income_upper":information.income_upper,
                "occupation":information.occupation,
                "education":information.education,
                "age":information.age,
                "purchase_times":information.purchase_times,
                }
        conn = self.conn_pool.connect()
        cursor = conn.cursor2()
        openid = information.openid
        key_array = []
        value_array = []
        for key in update_map:
            value = update_map[key]
            if value is not None:
                key_array.append(key)
                value_array.append(value)
        assert len(key_array) > 0
        try:
            sql = "update visitor set {0} where openid = {1}".format(','.join( x + "=%s" for x in key_array), openid)
            params = value_array * 2
            cursor.execute(sql, params)
            sql = "insert into visitor_record ({0}, openid) values ({1})".format(','.join(key_array), ','.join(["%s" % (len(key_array) + 1)]))
            params.append(openid)
            cursor.execute(sql, params)
            conn.commit()
            res.status = res.SUCCESS
        except Exception as e:
            conn.rollback()
            res.status = res.FAIL

        conn.close()
        return res
         
def start_server(config):
    server_config = config['server_redis']
    register_config = config['register_redis']
    mysql_db = config['mysql']
    service = UserService(**config)
    service.server_config = server_config
    service.register_config = register_config
    service.module_configs = {}
    signal.signal(signal.SIGTERM, service.stop)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    service.run()
