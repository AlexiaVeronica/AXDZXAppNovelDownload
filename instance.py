import re
import time
from config import *


class Vars:
    cfg = Config('Config.json', os.getcwd())
    book_info = None
    epub_info = None
    current_catalogue = None


class Msgs:
    msg_help = [
        "输入指令, 输入首字母即可 | 爱下电子书网址:https://m.aixdzs.com/",
        "d | bookid\t\t\t\t\t———输入书籍序号下载单本小说",
        "t | tagid\t\t\t\t\t———输入分类号批量下载分类小说",
        "n | bookname\t\t\t\t\t———下载单本小说",
        "h | help\t\t\t\t\t———获取使用程序帮助",
        "q | quit\t\t\t\t\t———退出运行的程序",
        "m | method\t\t\t\t\t———切换多线程和多进程",
        "p | pool\t\t\t\t\t———改变线程数目",
        "u | updata\t\t\t\t\t———下载指定文本中的bookid ",
    ]
    msg_agree_terms = '是否以仔细阅读且同意LICENSE中叙述免责声明\n如果同意声明，请输入英文 \"yes\" 或者中文 \"同意\" "\
            "后按Enter建，如果不同意请关闭此程式'
    msg_tag = {1: '玄幻', 2: '奇幻', 3: '武侠', 4: '仙侠', 5: '都市', 6: '职场', 7: '历史',
               8: '军事', 9: '游戏', 10: '竞技', 11: '科幻', 12: '灵异', 13: '同人', 14: '轻小说'}


def mkdir(file_path: [str, list]):
    if isinstance(file_path, list):
        for path in file_path:
            mkdir(path)
    else:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        return file_path


def inputs_(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


def write(path: str, mode: str, info=None):
    if info is not None:
        try:
            with open(path, f'{mode}', encoding='utf-8', newline='') as file:
                file.write(info)
        except (UnicodeEncodeError, UnicodeDecodeError) as error:
            print("error:", error)
            with open(path, f'{mode}', encoding='gbk', newline='') as file:
                file.write(info)
    else:
        try:
            return open(path, f'{mode}', encoding='utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            return open(path, f'{mode}', encoding='gbk')


def setup_config():
    Vars.cfg.load()
    config_change = False
    if type(Vars.cfg.data.get('save_book')) is not str or Vars.cfg.data.get('save_book') == "":
        Vars.cfg.data['save_book'] = 'novel'
        config_change = True
    if type(Vars.cfg.data.get('config_book')) is not str or Vars.cfg.data.get('config_book') == "":
        Vars.cfg.data['config_book'] = 'config'
        config_change = True
    if not isinstance(Vars.cfg.data.get('max_threads'), int):
        Vars.cfg.data['max_threads'] = 32
        config_change = True
    if type(Vars.cfg.data.get('real_time_cache')) is not bool:
        Vars.cfg.data['real_time_cache'] = False
        config_change = True
    if config_change:
        Vars.cfg.save()
