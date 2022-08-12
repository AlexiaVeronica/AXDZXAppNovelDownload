import requests
import tenacity
from src import UrlConstants
from instance import *


@tenacity.retry(stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_fixed(0.5))
def get(api_url: str, method: str = "GET", params: dict = None, app: bool = True, data_text: bool = False) -> "Request":
    headers = {
        "Keep-Alive": "300",
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
    }
    response = Request(url=api_url, method=method, data=params, data_text=data_text, headers=headers, app=app)
    response.request()
    return response


class Request:
    def __init__(self, url, data_text: bool, data: dict, method: str, headers: dict, app: bool):
        self.url = url
        self.app = app
        self.method = method
        self.headers = headers
        self.data_text = data_text
        self.data = data if data is not None else {}
        self.request_result = None

    @property
    def params(self):
        return json.dumps(self.data) if self.data_text else self.data

    @property
    def api_url(self) -> str:
        return UrlConstants.WEB_SITE + self.url if self.app else self.url

    @property
    def request_url(self):
        return self.request_result.url

    @property
    def json(self) -> dict:
        return self.request_result.json()

    @property
    def string(self) -> str:
        return self.request_result.text

    @property
    def content(self) -> bytes:
        return self.request_result.content

    @property
    def code(self) -> int:
        return self.request_result.status_code

    def retry(self, retry_max: int = 5, return_type: str = "json"):
        for retry in range(retry_max):
            if self.code == 200:
                if return_type == "json":
                    return self.json
                elif return_type == "string":
                    return self.string
                elif return_type == "content":
                    return self.content
            else:
                print("method:{}\t\tretry:{}\t\turl:{}".format(self.method, retry, self.request_url))
            self.request()  # 重试 request 操作
        return None

    def request(self):
        if self.method == "GET":
            self.request_result = requests.request(
                method=self.method, url=self.api_url, params=self.params, headers=self.headers
            )
        elif self.method == "POST" or self.method == "PUT":
            self.request_result = requests.request(
                method=self.method, url=self.api_url, data=self.params, headers=self.headers
            )
        else:
            raise Exception("method 【{}】 is not in ['GET', 'POST', 'PUT', 'DELETE']".format(self.method))
        return self.request_result
