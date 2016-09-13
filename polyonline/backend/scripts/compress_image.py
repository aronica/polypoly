#!/usr/bin/env python
#coding:utf8

import tinify
import os
import argparse
import json
import hashlib
from shutil import copyfile

def load_md5_file(filename):
    with open(filename) as fi:
        return json.load(fi)

def dump_md5_file(md5, filename):
    with open(filename, 'w') as fo:
        fo.write("{0}\n".format(json.dumps(md5, sort_keys = True)))

def generate_md5(filename):
    return hashlib.md5(open(filename, 'rb').read()).hexdigest()

def compress_file(infile, outfile):
    tinify.from_file(infile).to_file(outfile)
    infile_size = os.path.getsize(infile)
    outfile_size = os.path.getsize(outfile)
    print "compressed image from {0} to {1}, {2} reduced".format(infile_size, outfile_size, 1.0 * (infile_size - outfile_size)/infile_size)
    

tinify.key = "lT8hb3o34LdOlFOGcrAnylS4h88QZz-C"
md5_filename = "md5.json"

parser = argparse.ArgumentParser(description = "compress image")
parser.add_argument("inputdir", help = "input directory")
parser.add_argument("outputdir", help = "input directory")
args = parser.parse_args()
md5_file = os.path.join(args.inputdir, md5_filename)

md5 =  load_md5_file(md5_file)

image_format = ("png", "jpg", "jpeg")

if not os.path.exists(args.outputdir):
    os.makedirs(args.outputdir)

for root, sub_folders, files in os.walk(args.inputdir):
    for sub_folder in sub_folders:
        folder_name = os.path.join(root.replace(args.inputdir, args.outputdir, 1), sub_folder)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    for eachfile in files:
        print os.path.join(root, eachfile)
        if eachfile == md5_filename:
            continue
        if eachfile.split(".")[-1] in image_format:
            filename = os.path.join(root, eachfile)
            key = filename.replace(args.inputdir, "", 1)
            outputfile = filename.replace(args.inputdir, args.outputdir, 1)
            in_md5 = generate_md5(filename)
            if key not in md5 or md5[key][0] != in_md5 or not os.path.exists(outputfile):
                compress_file(filename, outputfile)
                md5[key] = [in_md5, generate_md5(outputfile)]
                dump_md5_file(md5, md5_file)
            else:
                out_md5 = generate_md5(outputfile)
                if out_md5 != md5[key][1]:
                    compress_file(filename, outputfile)
                    md5[key] = [in_md5, out_md5]
                    dump_md5_file(md5, md5_file)
        else:
            src = os.path.join(root, eachfile)
            dst = src.replace(args.inputdir, args.outputdir, 1)
            copyfile(src, dst)

