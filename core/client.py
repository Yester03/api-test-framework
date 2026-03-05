import requests
from config.config import BASE_URL, DEFAULT_TIMEOUT


class APIClient:
    def __init__(self):
        # 创建一个Sessonion对象
        self.session = requests.Session()
        self.base_url = BASE_URL

    # 封装同意请求方法, 内部使用
    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"

        response = self.session.request(
            method=method,
            url=url,
            timeout=DEFAULT_TIMEOUT,
            **kwargs,
        )

        return response

    # get方法
    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    # post方法
    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)
