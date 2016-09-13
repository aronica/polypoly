#!/usr/bin/env python
#coding:utf8

import redis

service_dict = {
        "http":("localhost", 8000),
        "poly":("localhost", 8000),
        "comment":("localhost", 8000),
        "visitor":("localhost", 8000),
        "operate":("localhost", 8000),
        "weixin":("localhost", 8000)
        }

register_redis_host = "localhost"
register_redis_port = 8000
r = redis.StrictRedis(host = register_redis_host, port = register_redis_port)
r.delete('service_dict')
for module_name in service_dict:
    host, port = service_dict[module_name]
    r.hset('service_dict', module_name, "{0}:{1}".format(host, port))
if __name__ == "__main__":
    pass
    

