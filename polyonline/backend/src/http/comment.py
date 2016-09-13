#!/usr/bin/env python
#coding:utf8

import http.wrapper as wrapper
import base.messages as message
import base.module as module
import StringIO
import xlwt
import json
import public_var
import logging
from base.tornado_client import greenlet_wrapper

class StructureCommentHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    @wrapper.check_url_parameter(['structure_id'])
    def post(self):
        self.do()

    def do(self):
        req = message.PolyCommentRequest()
        req.action = req.POST
        data = self.load_body()
        logging.info(json.dumps(data))
        req.property_id = self.get_argument('property_id', None)
        if req.property_id is not None:
            req.property_id = int(req.property_id)
        req.structure_id = int(self.get_argument('structure_id'))
        req.openid = data.get("openid", None)
        req.title = data.get("title", None)
        req.phone = data.get("phone", None)
        req.estimated_time = data.get("estimated_time", None)
        req.comment = message.StructureComment()
        req.comment.hall_score = data["comment"].get("hall_score", None)
        req.comment.kitchen_score = data["comment"].get("kitchen_score", None)
        req.comment.bedroom_score = data["comment"].get("bedroom_score", None)
        req.comment.toilet_score = data["comment"].get("toilet_score", None)
        req.comment.overview_score = data["comment"].get("overview_score", None)
        req.comment.hall_comment = data["comment"].get("hall_comment", None)
        req.comment.kitchen_comment = data["comment"].get("kitchen_comment", None)
        req.comment.bedroom_comment = data["comment"].get("bedroom_comment", None)
        req.comment.toilet_comment = data["comment"].get("toilet_comment", None)
        req.comment.overview_comment = data["comment"].get("overview_comment", None)
        res = self.send_call(module.MODULE_COMMENT, req)
        if res.status == res.SUCCESS:
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', None)
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)


class ExportHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    @wrapper.check_url_parameter(['city'])
    def get(self):
        self.do()

    def do(self):
        req = message.PolyCommentRequest()
        req.action = req.EXPORT
        req.city = self.get_argument("city")
        req.structure_name = self.get_argument("name", None)
        res = self.send_call(module.MODULE_COMMENT, req)
        if res.status == res.SUCCESS:
            f = StringIO.StringIO()
            if req.structure_name is None:
                filename = req.city
            else:
                filename = req.city + req.structure_name
            self.set_header("Content-Disposition", 'attachment;filename={0}.xls'.format(filename.encode("utf8")))
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("comment")
            header = [u"功能区", u"微信", u"手机", u"评论内容"]
            r = 0
            for c, name in enumerate(header):
                sheet.write(r, c, name)
            r += 1
            for result in res.comments:
                comment = result.get("comment")
                nickname = result.get("nickname", None)
                phone = result.get("phone", None)
                if nickname is None:
                    nickname = u"访客"
                    phone = u"访客"
                elif phone is None:
                    phone = u"未填写"
                if comment.hall_comment:
                    for c, name  in enumerate([u"客厅", nickname, phone, comment.hall_comment]):
                        sheet.write(r, c, name)
                    r += 1
                if comment.kitchen_comment:
                    for c, name  in enumerate([u"餐厅", nickname, phone, comment.kitchen_comment]):
                        sheet.write(r, c, name)
                    r += 1
                if comment.bedroom_comment:
                    for c, name  in enumerate([u"卧室", nickname, phone, comment.bedroom_comment]):
                        sheet.write(r, c, name)
                    r += 1
                if comment.toilet_comment:
                    for c, name  in enumerate([u"卫生间", nickname, phone, comment.toilet_comment]):
                        sheet.write(r, c, name)
                    r += 1
            workbook.save(f)
            self.write(f.getvalue())
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)
