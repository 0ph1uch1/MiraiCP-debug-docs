#!/usr/bin/env python3

'''
File: init.py
Project: MiraiCP-debug-docs
Author: Antares (antares0982@gmail.com)
-----
Copyright 2022 (c) Antares
'''


import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from typing import List


def try_remove_file(file: str):
    try:
        os.remove(file)
    except Exception:
        ...


def try_remove_tree(tree: str):
    try:
        shutil.rmtree(tree)
    except Exception:
        ...


def get_download_version(ver: str) -> str:
    return ver if ver[0] == 'v' else 'v'+ver


def get_version_in_foldername(ver: str) -> str:
    return ver[1:] if ver[0] == 'v' else ver

def readpipe_win32(command:List[str]):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
    while True:
        retcode = p.poll()
        print(p.stdout.readline())
        if retcode is not None:
            break

def main():
    if len(sys.argv) < 2:
        versionTag = "v2.12.0-RC"
    else:
        versionTag = sys.argv[1]

    compile = (len(sys.argv) >= 3 and sys.argv[2] == "compile")

    # download
    print(f"Downloading version {versionTag}")
    urllib.request.urlretrieve(
        f"https://github.com/Nambers/MiraiCP/archive/refs/tags/{get_download_version(versionTag)}.zip", "MiraiCP.zip")
    
    # extract
    try_remove_tree(f"MiraiCP-{get_version_in_foldername(versionTag)}")
    zipfile.ZipFile("MiraiCP.zip").extractall()
    os.remove("MiraiCP.zip")

    # move to root
    os.rename(f"MiraiCP-{get_version_in_foldername(versionTag)}", "MiraiCP")

    # copy necessary files
    try_remove_tree("src")
    shutil.copytree("MiraiCP/cpp/src", f"src")

    # create test cpp
    os.mkdir("src/plugin")
    shutil.copy("MiraiCP/cpp/demo/test.cpp", "src/plugin/test.cpp")

    # copy .clang-format
    try_remove_file(".clang-format")
    shutil.copy("MiraiCP/cpp/.clang-format", ".clang-format")
    
    # remove unnecessary files
    shutil.rmtree("MiraiCP")
    try_remove_tree("src/miraicp-core")
    try_remove_tree("src/examples")
    try_remove_tree("src/single_include")
    
    # compile
    if compile:
        try_remove_tree("build")
        os.mkdir("build")
        if sys.platform != 'win32':
            subprocess.check_output(
                ["cd build && cmake .. && make"], shell=True, encoding='utf-8')
        else:
            readpipe_win32(["cmake", "-B", "build", "."])
            readpipe_win32(["cmake", "--build", "build"])
        
        print("编译完成。")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("init failed, please check your working directory: is it MiraiCP-debug-docs?")
        raise e
