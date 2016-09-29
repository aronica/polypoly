#!/usr/bin/env python
#coding:utf8

import http.wrapper as wrapper
import base.messages as message
import base.module as module
import json
import re
import public_var
import StringIO
import xlwt
from base.tornado_client import greenlet_wrapper
from datetime import datetime

class CityListHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    def get(self):
        self.do()

    def do(self):
        req = message.PolyCityRequest()
        req.action = req.LIST
        res = self.send_call(module.MODULE_POLY, req)
        if res.status == res.SUCCESS:
            print(self.object2output(res))
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', self.object2output(res))
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)


    def object2output(self, res):
        result = {}
        result["count"] = len(res.cities)
        result["cities"] = res.cities
        return result

class PropertyListHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    @wrapper.check_url_parameter(['city'])
    def get(self):
        self.do()

    def do(self):
        req = message.PolyPropertyRequest()
        req.action = req.LIST
        req.city = self.get_argument('city')
        res = self.send_call(module.MODULE_POLY, req)
        if res.status == res.SUCCESS:
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', self.object2output(res))
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)


    def object2output(self, res):
        result = {}
        result["count"] = len(res.properties)
        result["properties"] = []
        for _property in res.properties:
            pd = {}
            pd["id"] = _property.id
            pd["name"] = _property.name
            pd["image"] = _property.image
            pd["description"] = _property.description
            pd["location"] = _property.location
            pd["isnew"] = _property.isnew;
            if _property.open_time_from:
                open_time_from = datetime.strptime( _property.open_time_from, "%Y-%m-%d %H:%M:%S")
                pd["open_time_from"] = "{0}年{1}月".format(open_time_from.year, open_time_from.month)
            else:
                pd["open_time_from"] = None
            if _property.open_time_to:
                open_time_to = datetime.strptime( _property.open_time_to, "%Y-%m-%d %H:%M:%S")
                pd["open_time_to"] = "{0}年{1}月".format(open_time_to.year, open_time_to.month)
            else:
                pd["open_time_to"] = None
            pd["property_age"] = "{0}年".format(_property.property_age)
            pd["surrounding"] = _property.surrounding
            result["properties"].append(pd)
        return result

class StructureFilterHandler(wrapper.BaseHandler):
    @greenlet_wrapper
    def get(self):
        self.do()

    def do(self):
        req = message.PolyStructureRequest()
        req.action = req.FILTER
        req.property_id = self.get_argument('property_id', None)
        res = self.send_call(module.MODULE_POLY, req)
        if res.status == res.SUCCESS:
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', self.object2output(res))
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)

    def object2output(self, res):
        result = {}
        result["area_filter"] = res.area_filter
        result["structure_filter"] = res.structure_filter
        return result


class StructureListHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    def get(self):
        self.do()

    def do(self):
        req = message.PolyStructureRequest()
        filters = message.StructureFilter()
        req.action = req.LIST
        property_id = self.get_argument('property_id', "")
        if property_id:
            req.property_id = int(property_id)

        room_count = self.get_argument('room_count', "")
        if room_count != "":
            filters.room_count = int(room_count)

        hall_count = self.get_argument('hall_count', "")
        if hall_count != "":
            filters.hall_count = int(hall_count)

        toilet_count = self.get_argument('toilet_count', "")
        if toilet_count != "":
            filters.toilet_count = int(toilet_count)

        lower_limit = self.get_argument('lower_limit', "")
        if lower_limit != "":
            filters.lower_limit = int(lower_limit)

        upper_limit = self.get_argument('upper_limit', "")
        if upper_limit != "":
            filters.upper_limit = int(upper_limit)

        req.filters = filters
        req.page = int(self.get_argument('page', 1))
        req.count = int(self.get_argument('count', 200))
        assert req.page > 0 and req.count > 0

        res = self.send_call(module.MODULE_POLY, req)
        if res.status == res.SUCCESS:
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', self.object2output(res))
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)

    def object2output(self, res):
        result = {}
        structures = {}
        structures["count"] = len(res.structure_list)
        structures["result"] = []
        for each in res.structure_list:
            structure = {}
            structure["id"] = each.id
            structure["name"] = each.name
            structure["area"] = each.area
            structure["image"] = each.image
            structure["room_count"] = each.room_count
            structure["hall_count"] = each.hall_count
            structure["toilet_count"] = each.toilet_count
            structures["result"].append(structure)
        result["structures"] = structures
        if res.property_info:
            property_info = {}
            property_info["id"] = res.property_info.id
            property_info["name"] = res.property_info.name
            property_info["image"] = res.property_info.image
            property_info["city"] = res.property_info.city
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
            result["property"] = property_info
        return result

class StructureDetailHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    @wrapper.check_url_parameter(['structure_id'])
    def get(self):
        self.do()

    def do(self):
        req = message.PolyStructureRequest()
        req.action = req.DETAIL
        req.structure_id = int(self.get_argument('structure_id'))
        property_id = self.get_argument('property_id', None)
        req.property_id = int(property_id) if property_id else None
        res = self.send_call(module.MODULE_POLY, req)
        if res.status == res.SUCCESS:
            self.make_return(public_var.RESULT_CODE_SUCCESS, 'success', self.object2output(res))
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)

    def object2output(self, res):
        result = {}
        result["name"] = res.structure.name
        result["area"] = res.structure.area
        result["image"] = res.structure.image
        result["room_count"] = res.structure.room_count
        result["hall_count"] = res.structure.hall_count
        result["toilet_count"] = res.structure.toilet_count
        result["hall_image"] = res.structure.hall_image
        result["kitchen_image"] = res.structure.kitchen_image
        result["bedroom_image"] = res.structure.bedroom_image
        result["toilet_image"] = res.structure.toilet_image
        result["position_image"] = res.structure.position_image
        result["sketchfab_id"] = res.structure.sketchfab_id
        result["720yun_id"] = res.structure.yun720_id
        return result

class ExportHandler(wrapper.BaseHandler):

    @greenlet_wrapper
    @wrapper.check_url_parameter(['city'])
    def get(self):
        self.do()

    def do(self):
        req = message.PolyStructureRequest()
        req.action = req.EXPORT
        req.city = self.get_argument("city")
        res = self.send_call(module.MODULE_POLY, req)
        if res.status == res.SUCCESS:
            f = StringIO.StringIO()
            filename = u"{0}户型数据".format(req.city)
            self.set_header("Content-Disposition", 'attachment;filename={0}.xls'.format(filename.encode("utf8")))
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("structure")
            header = [u"户型编号", u"类别", u"人气(点击量)", u"格局(S=室,T=厅,W=卫)", u"面积段", u"储备客户", u"评论意见"]
            r = 0
            for c, name in enumerate(header):
                sheet.write(r, c, name)
            r += 1
            for structure in res.structures:
                category = structure.name.split('-')[0][-1]
                pattern = "{0}S{1}T{2}W".format(structure.room_count, structure.hall_count, structure.toilet_count)
                for c, name in enumerate([structure.name, category, 0, pattern, structure.area, 0, 0]):
                    sheet.write(r, c, name)
                r += 1
            workbook.save(f)
            self.write(f.getvalue())
        else:
            self.make_return(public_var.RESULT_CODE_SERVER_ERROR, 'fail', None)


