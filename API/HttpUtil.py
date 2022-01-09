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

def get_cover(api_url):
    """封装get方法"""
    headers['User_Agent'] = random.choice(Vars.cfg.data.get('USER_AGENT_LIST'))
    try:
        return session.get(api_url, headers=headers).content
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


def get_dict_value(date, keys, default=None):
    keys_list = keys.split('.')
    if isinstance(date, dict):
        dictionary = dict(date)
        for i in keys_list:
            try:
                if dictionary.get(i) != None:
                    dict_values = dictionary.get(i)
                elif dictionary.get(i) == None:
                    dict_values = dictionary.get(int(i))
            except:
                return default
            dictionary = dict_values
        return dictionary
    else:
        try:
            dictionary = dict(eval(date))
            if isinstance(dictionary, dict):
                for i in keys_list:
                    try:
                        if dictionary.get(i) != None:
                            dict_values = dictionary.get(i)
                        elif dictionary.get(i) == None:
                            dict_values = dictionary.get(int(i))
                    except:
                        return default
                    dictionary = dict_values
                return dictionary
        except:
            return default
