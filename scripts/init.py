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


def main():
    if len(sys.argv) < 2:
        versionTag = "v2.12.0-RC"
    else:
        versionTag = sys.argv[1]

    compile = (len(sys.argv) >= 3 and sys.argv[2] == "compile")

    print(f"Downloading version {versionTag}")
    urllib.request.urlretrieve(
        f"https://github.com/Nambers/MiraiCP/archive/refs/tags/{get_download_version(versionTag)}.zip", "MiraiCP.zip")
    zipfile.ZipFile("MiraiCP.zip").extractall()
    os.remove("MiraiCP.zip")
    os.rename(f"MiraiCP-{get_version_in_foldername(versionTag)}", "MiraiCP")
    try_remove_tree("src")
    shutil.copytree("MiraiCP/cpp/src", f"src")
    try_remove_file(".clang-format")
    shutil.copy("MiraiCP/cpp/.clang-format", ".clang-format")
    shutil.rmtree("MiraiCP")
    try_remove_tree("src/miraicp-core")
    try_remove_tree("src/examples")
    try_remove_tree("src/single_include")
    os.mkdir("src/plugin")
    if compile:
        try_remove_tree("build")
        os.mkdir("build")
        subprocess.check_output(
            ["cd build && cmake .. && make"], shell=True, encoding='utf-8')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print("init failed, please check your working directory: is it MiraiCP-debug-docs?")
