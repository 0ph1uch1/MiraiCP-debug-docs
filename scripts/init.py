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

DEFAULT_VERSION_TAG = "v2.14.0"


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
        if p.stdout is not None:
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
    print("Extracting...")
    try_remove_tree(f"MiraiCP-{get_version_in_foldername(versionTag)}")
    zipfile.ZipFile("MiraiCP.zip").extractall()
    os.remove("MiraiCP.zip")

    # move to root
    print("Moving to root...")
    try_remove_tree("MiraiCP")
    os.rename(f"MiraiCP-{get_version_in_foldername(versionTag)}", "MiraiCP")

    # copy necessary files
    print("Copying necessary files...")
    try_remove_tree("src")
    shutil.copytree("MiraiCP/cpp/src", "src")
    try_remove_tree("include")
    shutil.copytree("MiraiCP/cpp/include", "include")
    try_remove_tree("3rd_include")
    shutil.copytree("MiraiCP/cpp/3rd_include", "3rd_include")

    # create test cpp
    print("Creating test source files...")
    os.mkdir("src/plugin")
    for file in os.listdir("MiraiCP/cpp/demo"):
        if file.find("single") != -1:
            continue
        shutil.copy(f"MiraiCP/cpp/demo/{file}", f"src/plugin/{file}")

    # copy .clang-format
    print("Copying .clang-format...")
    try_remove_file(".clang-format")
    shutil.copy("MiraiCP/cpp/.clang-format", ".clang-format")

    # remove unnecessary files
    print("Removing unnecessary files...")
    shutil.rmtree("MiraiCP")
    try_remove_tree("src/miraicp-core")
    try_remove_tree("src/examples")
    try_remove_tree("src/single_include")

    # create build
    print("Creating build folder...")
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
        text = """
初始化失败，请检查：
1. 工作目录是否是: MiraiCP-debug-docs？
2. 如果文件夹创建失败，请检查您的IDE是否已经关闭（仅限Windows）
3. 是否将本git仓库切换到对应分支的tag？
4. 如果上述均检查完成，将本仓库下载、生成的所有文件全部清理掉后再试。
5. 如果上述均检查完成，请向本仓库提交issue。
        """
        print(text)
        raise e
