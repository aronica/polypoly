# -*- coding:utf-8 -*-

import logging
import json
import signal
import datetime
import base.module as module
import util.connection_pool as connection_pool
from base.async_server import AsyncService, async_method
from base.messages import *
from util.common_util import *

class PolyService(AsyncService):
    def __init__(self, **kwargs):
        super(PolyService, self).__init__(module.MODULE_POLY, **kwargs)
        mysql_config = kwargs["mysql"]
        self.conn_pool = connection_pool.MySQLConnectionPool(host = mysql_config['host'], user = mysql_config['user'], passwd = mysql_config['pwd'], db = mysql_config['db'])


    def on_call_PolyCityRequest(self, pkg):
        if pkg.action == pkg.LIST:
            return self.list_city()

    def on_call_PolyPropertyRequest(self, pkg):
        if pkg.action == pkg.LIST:
            return self.list_property(pkg.city)
        elif pkg.action == pkg.DESCRIBE:
            return self.describe_property(pkg.property_id)

    def on_call_PolyStructureRequest(self, pkg):
        if pkg.action == pkg.LIST:
            return self.list_structure(pkg.property_id, pkg.filters, pkg.page, pkg.count)
        elif pkg.action == pkg.FILTER:
            return self.get_structure_filter(pkg.property_id)
        elif pkg.action == pkg.DETAIL:
            return self.get_structure_detail(pkg.property_id, pkg.structure_id)
        elif pkg.action == pkg.EXPORT:
            return self.export_structure(pkg.city)
        else:
            assert False

    def list_city(self):
        res = PolyCityResponse()
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        sql = "select distinct(city) from property where shown = 1"
        cursor.execute(sql)
        for city in cursor.fetchall():
            res.cities.append(city[0])
        res.cities.sort()
        res.status = res.SUCCESS
        conn.close()
        return res

    def list_property(self, city):
        res = PolyPropertyResponse()
        res.status = res.SUCCESS
        res.properties = []
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        logging.debug(city)
        if city:
            sql = "select id, name, city, image, description, location, open_time_from, open_time_to, property_age, surrounding,isnew from property where city = %s and shown = 1 order by isnew desc,open_time_from desc"
            params = (city, )
            cursor.execute(sql, params)
        else:
            sql = "select id, name, city, image, description, location, open_time_from, open_time_to, property_age, surrounding,isnew from property where shown = 1 order by isnew desc,open_time_from desc"
            cursor.execute(sql)
        for item in cursor.fetchall():
            _property = PolyProperty()
            _property.id = item[0]
            _property.name = item[1]
            _property.city = item[2]
            _property.image = json.loads(item[3])
            _property.description = item[4]
            _property.location = item[5]
            _property.open_time_from = item[6]
            _property.open_time_to = item[7]
            _property.property_age = item[8]
            _property.surrounding = json.loads(item[9])
            _property.isnew=item[10]
            res.properties.append(_property)
        conn.close()
        return res

    def describe_property(self, property_id):
        if property_id is None:
            return None
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        sql = "select name, city, image, description, location, open_time_from, open_time_to, property_age, surrounding,isnew from property where id = %s"
        params = [property_id]
        cursor.execute(sql, params)
        assert cursor.rowcount == 1
        item = cursor.fetchone()
        _property = PolyProperty()
        _property.id = property_id
        _property.name = item[0]
        _property.city = item[1]
        _property.image = json.loads(item[2])
        _property.description = item[3]
        _property.location = item[4]
        _property.open_time_from = item[5]
        _property.open_time_to = item[6]
        _property.property_age = item[7]
        _property.surrounding = json.loads(item[8])
        _property.isnew = item[9]
        conn.close()
        return _property

    def get_structure_filter(self, property_id):
        area_filter_set = set()
        structure_filter_set = set()
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        if property_id == None:
            sql = "select area, room_count, hall_count, toilet_count from structure where shown = 1"
            cursor.execute(sql)
        else:
            sql = "select s.area, s.room_count, s.hall_count, s.toilet_count from property_structure as ps, structure as s where ps.property_id = %s and ps.structure_id = s.id and s.shown = 1"
            params = (property_id, )
            cursor.execute(sql, params)
        for item in cursor.fetchall():
            area, room_count, hall_count, toilet_count = item
            for each in get_area_filter(int(area)):
                area_filter_set.add(each)
            structure_filter_set.add((room_count, hall_count, toilet_count))
        res = PolyStructureResponse()
        res.status = res.SUCCESS
        res.area_filter = []
        res.structure_filter = []
        if area_filter_set:
            res.area_filter = sorted(list(area_filter_set))
        if structure_filter_set:
            res.structure_filter = sorted(list(structure_filter_set))
        conn.close()
        return res

    def list_structure(self, property_id, filters, page, count):
        res = PolyStructureResponse()
        res.status = res.SUCCESS
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        if property_id is None:
            sql = 'select id, name, area, image, room_count, hall_count, toilet_count from structure where shown = 1 order by area, name'
            cursor.execute(sql)
        else:
            sql = 'select s.id, s.name, s.area, s.image, s.room_count, s.hall_count, s.toilet_count from structure as s, property_structure as ps where ps.property_id = %s and ps.structure_id = s.id and s.shown = 1 order by s.area, s.name'
            cursor.execute(sql, [property_id])
        total = 0
        lower = (page - 1) * count
        upper = lower + count
        for each in cursor.fetchall():
            sid, name, area, image, room_count, hall_count, toilet_count = each
            if filters.room_count not in (room_count, None) or filters.hall_count not in (hall_count, None) or filters.toilet_count not in (toilet_count, None):
                continue
            if filters.lower_limit is not None and area < filters.lower_limit:
                continue
            if filters.upper_limit not in (None, -1) and area > filters.upper_limit:
                continue
            total += 1
            if lower < total <= upper:
                structure  = PolyStructure()
                structure.id = sid
                structure.name = name
                structure.area = area
                structure.image = image
                structure.room_count = room_count
                structure.hall_count = hall_count
                structure.toilet_count = toilet_count
                res.structure_list.append(structure)
            elif total > upper:
                break
        res.property_info = self.describe_property(property_id)
        conn.close()
        return res

    def get_structure_detail(self, property_id, structure_id):
        res = PolyStructureDetailResponse()
        res.status = res.FAIL
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        sql = "select name, area, image, room_count, hall_count, toilet_count, hall_image, kitchen_image, bedroom_image, toilet_image, position_image, sketchfab_id, 720yun_id from structure where id = %s"
        params = [structure_id]
        cursor.execute(sql,params)
        s = PolyStructure()
        if cursor.rowcount == 1:
            res.status = res.SUCCESS
            s.name, s.area, s.image, s.room_count, s.hall_count, s.toilet_count, s.hall_image , s.kitchen_image, s.bedroom_image, s.toilet_image, s.position_image, s.sketchfab_id, s.yun720_id = cursor.fetchone()
        else:
            assert cursor.rowcount == 0
            res.status = res.EMPTY
        try:
            if res.status == res.SUCCESS:
                sql = "insert into structure_statistic (dt, property_id, structure_id) values (%s, %s, %s) on duplicate key update popularity = popularity + 1"
                params = [datetime.date.today(), property_id if property_id else -1, structure_id]
                cursor.execute(sql, params)
        except Exception as e:
            logging.error(e, exc_info = True)
        res.structure = s
        conn.close()
        return res

    def export_structure(self, city):
        res = ExportStructureResponse()
        res.status = res.FAIL
        res.structures = []
        conn = self.conn_pool.connect()
        cursor = conn.cursor()
        sql = "select s.name, s.room_count, s.hall_count, s.toilet_count, s.area from property as p, property_structure as ps, structure as s where p.city = %s and p.id = ps.property_id and ps.structure_id = s.id group by s.name order by s.area, s.name"
        params = [city]
        cursor.execute(sql, params)
        for each in cursor.fetchall():
            s = PolyStructure()
            s.name, s.room_count, s.hall_count, s.toilet_count, s.area = each
            res.structures.append(s)
        res.status = res.SUCCESS
        conn.close()
        return res


def start_server(config):
    server_config = config['server_redis']
    register_config = config['register_redis']
    mysql_db = config['mysql']
    service = PolyService(**config)
    service.server_config = server_config
    service.register_config = register_config
    service.module_configs = {}
    signal.signal(signal.SIGTERM, service.stop)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    service.run()

