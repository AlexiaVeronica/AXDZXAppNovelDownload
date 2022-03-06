import requests
from instance import *
import functools
from fake_useragent import UserAgent

session = requests.session()


def MaxRetry(func, max_retry=5):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for retry in range(max_retry):
            response = func(*args, **kwargs)
            if not isinstance(response, bool):
                return response
            else:
                print("尝试第:{}次".format(retry + 1))
                time.sleep(retry * 0.5)

    return wrapper


def headers():
    return {
        "Keep-Alive": "300",
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip",
        'User-Agent': UserAgent(verify_ssl=False).random,
    }


@MaxRetry
def get(api_url: str, params=None, **kwargs):
    try:
        response = requests.get(api_url, headers=headers(), params=params, **kwargs)
        if response.status_code == 200:
            return response
        else:
            return False
    except requests.exceptions.RequestException as error:
        print("\nGet url:{} Error:{}".format(api_url, error))
        return False


@MaxRetry
def post(api_url: str, data=None, **kwargs):
    try:
        response = requests.post(api_url, headers=headers(), params=data, **kwargs)
        if response.status_code == 200:
            return response
        else:
            return False
    except requests.exceptions.RequestException as error:
        print("\nGet url:{} Error:{}".format(api_url, error))
        return False


@MaxRetry
def put(api_url: str, data=None, **kwargs):
    try:
        response = requests.put(api_url, headers=headers(), params=data, **kwargs)
        if response.status_code == 200:
            return response
        else:
            return False
    except requests.exceptions.RequestException as error:
        print("\nGet url:{} Error:{}".format(api_url, error))
        return False
