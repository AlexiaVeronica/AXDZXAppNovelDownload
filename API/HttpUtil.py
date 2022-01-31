import random
import requests
from function.instance import *


def headers():
    return {
        "Keep-Alive": "300",
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip",
        "User-Agent": random.choice(Vars.cfg.data.get('USER_AGENT_LIST'))
    }


session = requests.session()


def get(api_url, max_retry=10):
    for count in range(max_retry):
        try:
            return session.get(api_url, headers=headers()).json()
        except (OSError, TimeoutError, IOError) as error:
            time.sleep(0.5 * count)
    else:
        print(f"\nGet Failed:{api_url}\nTerminating......")
        sys.exit(1)


def post(api_url, data=None, max_retry=10):
    for count in range(max_retry):
        try:
            return session.post(api_url, data=data, headers=headers()).json()
        except (OSError, TimeoutError, IOError) as error:
            print(f"\nGet Error Retry {count + 1}: " + api_url)
            time.sleep(0.5 * count)
    else:
        print(f"\nGet Failed:{api_url}\nTerminating......")
        sys.exit(1)


def cover(api_url: str, max_retry=10):
    for count in range(max_retry):
        try:
            return requests.get(api_url, headers=headers())
        except (OSError, TimeoutError, IOError) as error:
            print(f"\nGet Error Retry {count + 1}: " + api_url)
            time.sleep(0.5 * count)
    else:
        print(f"\nGet Failed:{api_url}\nTerminating......")
        sys.exit(1)


def put(api_url, data=None, max_retry=10):
    for count in range(max_retry):
        try:
            return session.put(api_url, data=data, headers=headers()).json()
        except (OSError, TimeoutError, IOError) as error:
            print(f"\nGet Error Retry {count + 1}: " + api_url)
            time.sleep(0.5 * count)
    else:
        print(f"\nGet Failed:{api_url}\nTerminating......")
        sys.exit(1)
