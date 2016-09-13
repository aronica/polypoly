#coding=utf8
"""
# author: Ke Wu
# created_time: 2016-08-16 19:14:53
# file_name: store_imgs.py
# description:
"""

import os
import sys
from shutil import copyfile, copy2


if __name__ == '__main__':
    src = sys.argv[1]
    des = sys.argv[2]


    print u'源文件：', src
    print u'目标文件夹：', des

    files = os.listdir(src)
    print u'源文件夹所有文件'
    print files

    for f in files:
        if f.endswith('.jpg'):
            print u'正在复制文件：', f
            filename = f.replace('-450-350.jpg', '')
            directory = des + '/' + filename

            if not os.path.exists(directory):
                os.makedirs(directory)
            copy2(src + '/' + f, directory)
        else:
            print u'跳过文件：', f
    print u'完成'
