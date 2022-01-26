import random
import requests
from function.instance import *

headers = {
    "Keep-Alive": "300",
    "Connection": "Keep-Alive",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip",
}

session = requests.Session()


def get(api_url):
    """封装get方法"""
    headers['User_Agent'] = random.choice(Vars.cfg.data.get('USER_AGENT_LIST'))
    try:
        return session.get(api_url, headers=headers).json()
    except Exception as e:
        print("get请求错误:", e)
        pass


def cover(api_jsno: dict):
    headers['User_Agent'] = random.choice(Vars.cfg.data.get('USER_AGENT_LIST'))
    try:
        return requests.get(api_jsno.get('acgurl'), headers=headers).content
    except Exception as e:
        print("get请求错误:", e)
        pass


def post(api_url, data=None):
    """封装post方法"""
    headers['User_Agent'] = random.choice(
        Vars.cfg.data.get('USER_AGENT_LIST'))
    try:
        return session.post(api_url, data, headers=headers).json()
    except Exception as e:
        print("post请求错误:", e)


def put(api_url, data=None):
    """封装put方法"""
    headers['User_Agent'] = random.choice(
        Vars.cfg.data.get('USER_AGENT_LIST'))
    try:
        return session.put(api_url, data, headers=headers).json()
    except Exception as e:
        print("put请求错误:", e)

