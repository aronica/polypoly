#!/usr/bin/env python
#coding:utf8

import http.wrapper as wrapper
import base.messages as message
import base.module as module
import json
import public_var
from base.tornado_client import greenlet_wrapper
from datetime import datetime

class InformationSetHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    def post(self):
        self.do()

    def do(self):
        req = message.UserInformationRequest()
        req.action = req.UPDATE
        data = self.load_body()
        information = UserInformation()
        information.openid = data.get("openid")
        information.phone = data.get("phone", None)
        information.family_structure = data.get("family_structure", None)
        information.income_lower = data.get("income_lower", None)
        information.income_upper = data.get("income_upper", None)
        information.occupation = data.get("occupation", None)
        information.education = data.get("education", None)
        information.age = data.get("age", None)
        information.purchase_times = data.get("purchase_times", None)
        req.user_information = information
        res = self.send_call(module.MODULE_VISITOR, req)
        if res.status == res.SUCCESS:
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', None)
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)

class StructureGetHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    @wrapper.check_url_parameter(['openid'])
    def get(self):
        self.do()

    def do(self):
        res = message.UserStructureResponse()
        res.status = res.FAIL
        fail_info = "fail"
        comment_req = message.PolyCommentRequest()
        comment_req.action = comment_req.GET
        comment_req.openid = self.get_argument("openid")
        comment_res = self.send_call(module.MODULE_COMMENT, comment_req)
        if comment_res.status == comment_res.SUCCESS:
            res.comment = comment_res.comment
            if comment_res.property_id is not None:
                property_req = message.PolyPropertyRequest()
                property_req.action = property_req.DESCRIBE
                property_req.property_id = comment_res.property_id
                property_res = self.send_call(module.MODULE_POLY, property_req)
                res.property_info = property_res
            structure_req = message.PolyStructureRequest()
            structure_req.action = structure_req.DETAIL
            structure_req.structure_id = comment_res.structure_id
            structure_res = self.send_call(module.MODULE_POLY, structure_req)
            if structure_res.status == structure_res.SUCCESS:
                res.status = res.SUCCESS
                res.structure = structure_res.structure
            else:
                fail_info = "structure not found"
        else:
            fail_info = "comment not found"
        if res.status == res.SUCCESS:
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', self.object2output(res))
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, fail_info, None)

    def object2output(self, res):
        result = {}
        structure = {}
        property_info = {}
        comment = {}
        if res.comment is not None:
            comment["hall_comment"] = res.comment.hall_comment
            comment["kitchen_comment"] = res.comment.hall_comment
            comment["bedroom_comment"] = res.comment.bedroom_comment
            comment["toilet_comment"] = res.comment.toilet_comment
            comment["overview_comment"] = res.comment.overview_comment
        if res.structure is not None:
            structure["name"] = res.structure.name
            structure["image"] = res.structure.image
            structure["area"] = res.structure.area
            structure["room_count"] = res.structure.room_count
            structure["hall_count"] = res.structure.hall_count
            structure["toilet_count"] = res.structure.toilet_count
        if res.property_info is not None:
            property_info["id"] = res.property_info.id
            property_info["name"] = res.property_info.name
            property_info["image"] = res.property_info.image
            property_info["description"] = res.property_info.description
            property_info["location"] = res.property_info.location
            if res.property_info.open_time_from:
                open_time_from = datetime.strptime(res.property_info.open_time_from, "%Y-%m-%d %H:%M:%S")
                property_info["open_time_from"] = "{0}年{1}月".format(open_time_from.year, open_time_from.month)
            else:
                property_info["open_time_from"] = None
            if res.property_info.open_time_to:
                open_time_to = datetime.strptime(res.property_info.open_time_to, "%Y-%m-%d %H:%M:%S")
                property_info["open_time_to"] = "{0}年{1}月".format(open_time_to.year, open_time_to.month)
            else:
                property_info["open_time_to"] = None
            property_info["property_age"] = "{0}年".format(res.property_info.property_age)
            property_info["surrounding"] = res.property_info.surrounding
        result["comment"] = comment
        result["property"] = property_info
        result["structure"] = structure
        return result

class ExportHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    def get(self):
        self.do()

    def do(self):
        if res.status == res.SUCCESS:
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', None)
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)


class WeixinInfoSetHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    def post(self):
        self.do()

    def do(self):
        req = message.WeixinUserInfo()
        req.action = req.SET
        data = self.load_body()
        req.openid = data.get("openid", None)
        req.unionid = data.get("unionid", None)
        req.nickname = data.get("nickname", None)
        req.headimgurl = data.get("headimgurl", None)
        req.sex = data.get("sex", None)
        req.lang = data.get("language", None)
        req.country = data.get("country", None)
        req.province = data.get("province", None)
        req.city = data.get("city", None)
        req.privilege = data.get("privilege", [])
        if req.openid is None:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)
        else:
            res = self.send_call(module.MODULE_WEIXIN, req)
            if res.status == res.SUCCESS:
                self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', None)
            else:
                self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)

class WeixinInfoGetHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    @wrapper.check_url_parameter(['openid'])
    def get(self):
        self.do()

    def do(self):
        req = message.WeixinUserInfo()
        req.action = req.GET
        req.openid = self.get_argument("openid")
        res = self.send_call(module.MODULE_WEIXIN, req)
        if res.status == res.SUCCESS:
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', self.object2output(res))
        elif res.status == res.NO_USER:
            self.make_return(public_var.RESULT_CODE_USER_NOT_FOUND, 'user not found', None)
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)

    def object2output(self, res):
        return {
                "openid":res.openid,
                "nickname":res.nickname,
                "headimgurl":res.headimgurl
                }
