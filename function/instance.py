from .config import *
import os
import re
import time
import sys
from rich import print


class Vars:
    cfg = Config('Config.json', os.getcwd())
    current_bookshelf = None
    current_book = None


def mkdir(file_path: str):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def makedirs(file_path: str):
    if not os.path.exists(os.path.join(file_path)):
        os.makedirs(os.path.join(file_path))


def time_(time_stamp: int):
    if type(time_stamp) is not int:
        time_stamp = int(time_stamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(_time_))


def inputs_(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


def del_title(title: str):
    """删去windowns不规范字符"""
    return re.sub(r'[？?\*|“<>:/\\]', '', title)


def content_(content: str):
    return ''.join([re.sub(r'^\s*', "\n　　", content)
                    for content in content.split("\n") if re.search(r'\S', content) != None])


def write(path: str, mode: str, info=None):
    if info is not None:
        try:
            with open(path, f'{mode}', encoding='UTF-8', newline='') as file:
                file.writelines(info)
        except (UnicodeEncodeError, UnicodeDecodeError)as e:
            print(e)
            with open(path, f'{mode}', encoding='gbk', newline='') as file:
                file.writelines(info)
    else:
        try:
            file = open(path, f'{mode}', encoding='UTF-8')
            return file
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            print(e)
            file = open(path, f'{mode}', encoding='gbk')
            return file
