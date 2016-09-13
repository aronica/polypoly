#!/usr/bin/env python
#coding:utf8

AREA_INTERVAL = (
        (70, 90),
        (90, 100),
        (100, 120),
        (120, 140),
        (140, -1),
        )

def get_area_filter(area):
    for each in AREA_INTERVAL:
        if each[1] == -1 and area >= each[0]:
            yield each
        elif each[0] <= area <= each[1]:
            yield each
