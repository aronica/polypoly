#!/usr/bin/env python
#coding:utf8

import argparse
import MySQLdb
import json
from datetime import datetime

mysql_config = {
        "db":"polyonline",
        "host":"localhost",
        "user":"puju",
        "passwd":"puju",
        }

def get_args():
    parser = argparse.ArgumentParser(description = "load polydata")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--property', help = "load property data")
    group.add_argument('-s', '--structure', help = "load structure data")
    return parser.parse_args()

def load_property(filename):
    conn = MySQLdb.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute('set names utf8;')
    cursor.execute('set character set utf8;')
    cursor.execute('set character_set_connection=utf8;')
    property_sql = "insert ignore into property (city, name, description, image, location, open_time_from , open_time_to, property_age, surrounding) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    relationship_sql = "insert ignore into property_structure (property_id, structure_id) values (%s, %s)"
    id_sql = "select property.id, structure.id from property, structure where property.city = %s and property.name = %s and structure.name = %s"
    with open(filename) as fi:
        property_list = json.load(fi)
        for property_info in property_list:
            city, name, description, location, open_time_from, open_time_to, property_age, surrounding, structure, image = None, None, None, None, None, None, None, [], [], []
            city = property_info["city"].encode("utf8")
            name = property_info["name"].encode("utf8")
            description = property_info["description"].encode("utf8")
            location = property_info["location"].encode("utf8")
            open_time = property_info["open_time"].encode("utf8")
            property_age = property_info["property_age"]
            surrounding = json.dumps([u"医院", u"购物中心", u"学校"])
            structure = property_info.get("structure", [])
            image = json.dumps(property_info.get("image", []))
            params = [city, name, description, image, location, open_time_from, open_time_to, property_age, surrounding]
            cursor.execute(property_sql, params)
            conn.commit()
            for s in structure:
                print city, name, s
                params = (city, name, s)
                cursor.execute(id_sql, params)
                pid, sid = cursor.fetchone()
                params = (pid, sid)
                cursor.execute(relationship_sql, params)
                conn.commit()
    conn.close()

def load_structure(filename):
    conn = MySQLdb.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute('set names utf8;')
    cursor.execute('set character set utf8;')
    cursor.execute('set character_set_connection=utf8;')
    key_array = ["name", "area", "room_count", "hall_count", "toilet_count", "lowest_price", "image", "hall_image", "kitchen_image", "bedroom_image", "toilet_image", "position_image", "sketchfab_id", "720yun_id"]
    assert key_array[0] == "name"
    sql = "insert ignore into structure ({0}) values ({1}) on duplicate key update {2}".format(",".join(key_array), ",".join(["%s"] * len(key_array)), ",".join("{0} = %s".format(x) for x in key_array[1:]))
    with open(filename) as fi:
        structure_list = json.load(fi)
        for structure in structure_list:
            params = [structure[x] for x in key_array]
            params += params[1:]
            params = (x if x != "" else None for x in params)
            cursor.execute(sql, params)
    conn.commit()
    conn.close()

def main():
    args = get_args()
    if args.property:
        load_property(args.property)
    elif args.structure:
        load_structure(args.structure)

if __name__ == "__main__":
    main()
