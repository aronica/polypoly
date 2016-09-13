# -*- coding:utf-8 -*-

import logging
import json
import signal
import base.module as module
import util.connection_pool as connection_pool
from base.async_server import AsyncService, async_method
from base.messages import *

class CommentService(AsyncService):
    def __init__(self, **kwargs):
        super(CommentService, self).__init__(module.MODULE_COMMENT, **kwargs)
        mysql_config = kwargs["mysql"]
        self.conn_pool = connection_pool.MySQLConnectionPool(host = mysql_config['host'], user = mysql_config['user'], passwd = mysql_config['pwd'], db = mysql_config['db'])

    def on_call_PolyCommentRequest(self, pkg):
        if pkg.action == pkg.POST:
            return self.comment_structure(pkg)
        if pkg.action == pkg.GET:
            return self.get_comment(pkg)
        if pkg.action == pkg.EXPORT:
            return self.export_comment(pkg.city, pkg.structure_name)

    def get_unionid_by_openid(self, openid):
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        sql = "select unionid from weixin_profile where openid = %s limit 1"
        params = [openid]
        cursor.execute(sql, params)
        unionid = cursor.fetchone()[0] if cursor.rowcount else None
        conn.close()
        return unionid

    def comment_structure(self, pkg):
        res = PostResponse()
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        structure_id = pkg.structure_id
        property_id = pkg.property_id
        openid = pkg.openid
        assert openid
        title = pkg.title
        phone = pkg.phone
        estimated_time = pkg.estimated_time
        comment = pkg.comment
        unionid = self.get_unionid_by_openid(openid)
        sql = "insert into comments (openid, unionid, title, phone, property_id, structure_id, hall_score, hall_comment, kitchen_score, kitchen_comment, bedroom_score, bedroom_comment, toilet_score, toilet_comment, overview_score, overview_comment, estimated_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = [openid, unionid, title, phone, property_id, structure_id, comment.hall_score, comment.hall_comment, comment.kitchen_score, comment.kitchen_comment, comment.bedroom_score, comment.bedroom_comment, comment.toilet_score, comment.toilet_comment, comment.overview_score, comment.overview_comment, estimated_time]
        cursor.execute(sql, params)
        conn.close()
        res.status = res.SUCCESS
        return res

    def get_comment(self, pkg):
        res = PolyCommentResponse()
        res.status = res.FAIL
        unionid = self.get_unionid_by_openid(pkg.openid)
        if not unionid:
            return res
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        sql = "select property_id, structure_id, hall_comment, kitchen_comment, bedroom_comment, toilet_comment, overview_comment from comments where unionid = %s and property_id is not NULL order by ts desc limit 1"
        params = [unionid]
        cursor.execute(sql, params)
        if cursor.rowcount == 0:
            res.status = res.NO_COMMENT
        elif cursor.rowcount == 1:
            res.status = res.SUCCESS
            item = cursor.fetchone()
            res.property_id = item[0]
            res.structure_id = item[1]
            comment = StructureComment()
            comment.hall_comment = item[2]
            comment.kitchen_comment = item[3]
            comment.bedroom_comment = item[4]
            comment.toilet_comment = item[5]
            comment.overview_comment = item[6]
            res.comment = comment
        conn.close()
        return res

    def export_comment(self, city, name):
        res = ExportCommentResponse()
        res.status = res.FAIL
        res.comments = []
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        if name is None:
            sql = 'select w.nickname, c.phone, c.hall_comment, c.kitchen_comment, c.bedroom_comment, c.toilet_comment from comments as c, weixin_profile as w where c.property_id in (select id from property where city = %s) and (c.openid = NULL or c.openid = w.openid)'
            params = [city]
        else:
            sql = 'select w.nickname, c.phone, c.hall_comment, c.kitchen_comment, c.bedroom_comment, c.toilet_comment from comments as c, weixin_profile as w where c.property_id in (select id from property where city = %s) and c.structure_id in (select id from structure where name = %s)  and (c.openid = NULL or c.openid = w.openid)'
            params = [city, name]
        cursor.execute(sql, params)
        for each in cursor.fetchall():
            nickname , phone, hall_comment, kitchen_comment, bedroom_comment, toilet_comment = each
            comment = StructureComment()
            comment.hall_comment = hall_comment
            comment.kitchen_comment = kitchen_comment
            comment.bedroom_comment = bedroom_comment
            comment.toilet_comment = toilet_comment
            res.comments.append({"comment":comment, "nickname":nickname, "phone":phone})
        res.status = res.SUCCESS
        conn.close()
        return res

def start_server(config):
    server_config = config['server_redis']
    register_config = config['register_redis']
    mysql_db = config['mysql']
    service = CommentService(**config)
    service.server_config = server_config
    service.register_config = register_config
    service.module_configs = {}
    signal.signal(signal.SIGTERM, service.stop)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    service.run()
