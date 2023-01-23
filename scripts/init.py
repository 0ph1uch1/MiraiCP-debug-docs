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

DEFAULT_VERSION_TAG = "v2.13.1"


def try_remove_file(file: str):
    try:
        os.remove(file)
    except Exception:
        ...


def try_remove_tree(tree: str):
    try:
        shutil.rmtree(tree)
    except PermissionError as e:
        raise e
    except Exception:
        ...


def try_mkdir(dir: str):
    try:
        os.mkdir(dir)
    except Exception:
        ...


def get_download_version(ver: str) -> str:
    return ver if ver[0] == 'v' else 'v'+ver


def get_version_in_foldername(ver: str) -> str:
    return ver[1:] if ver[0] == 'v' else ver


def readpipe_win32(command: List[str]):
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, encoding='gbk')
    while True:
        retcode = p.poll()
        print(p.stdout.readline())
        if retcode is not None:
            break


def main():
    if len(sys.argv) < 2:
        versionTag = DEFAULT_VERSION_TAG
    else:
        versionTag = sys.argv[1]

    compile = (len(sys.argv) >= 3 and sys.argv[2] == "compile")

    # download
    print(f"Downloading version {versionTag}")
    try:
        urllib.request.urlretrieve(
            f"https://github.com/Nambers/MiraiCP/archive/refs/tags/{get_download_version(versionTag)}.zip", "MiraiCP.zip")
    except Exception:
        try_remove_file("MiraiCP.zip")
        urllib.request.urlretrieve(
            f"https://ghproxy.com/https://github.com/Nambers/MiraiCP/archive/refs/tags/{get_download_version(versionTag)}.zip", "MiraiCP.zip")

    # extract
    try_remove_tree(f"MiraiCP-{get_version_in_foldername(versionTag)}")
    zipfile.ZipFile("MiraiCP.zip").extractall()
    os.remove("MiraiCP.zip")

    # move to root
    os.rename(f"MiraiCP-{get_version_in_foldername(versionTag)}", "MiraiCP")

    # copy necessary files
    try_remove_tree("src")
    shutil.copytree("MiraiCP/cpp/src", "src")
    try_remove_tree("include")
    shutil.copytree("MiraiCP/cpp/include", "include")
    try_remove_tree("3rd_include")
    shutil.copytree("MiraiCP/cpp/3rd_include", "3rd_include")

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

    # create build
    try_mkdir("build")
    if sys.platform != "win32":
        subprocess.check_output(
            ["cd build && cmake .."], shell=True, encoding='utf-8')
    else:
        readpipe_win32(["cmake", "-B", "build", "."])

    print("CMake项目生成完成。")

    # compile
    if compile:
        if sys.platform != 'win32':
            subprocess.check_output(
                ["cd build && make"], shell=True, encoding='utf-8')
        else:
            readpipe_win32(["cmake", "--build", "build"])

        print("编译完成。")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("初始化失败，如果遇到路径问题，请检查工作目录是否是: MiraiCP-debug-docs？\n如果文件夹创建失败，请检查您的IDE是否已经关闭（仅限Windows）")
        raise e
