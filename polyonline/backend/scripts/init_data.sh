#!/usr/bin/env bash
mysql -upuju -ppuju < ../sql/polyonline.sql
python load_data.py -s ../res/structure.json
python load_data.py -p ../res/property.json
