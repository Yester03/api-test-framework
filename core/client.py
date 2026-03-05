import requests
from config.config import BASE_URL, DEFAULT_TIMEOUT


class APIClient:
    def __init__(self):
        # 创建一个Sessonion对象
        self.session = requests.Session()
        self.base_url = BASE_URL.rstrip("/")

    # 封装同意请求方法, 内部使用
    def request(self, method: str, path: str, **kwargs):
        """
        统一请求入口：拼接 base_url + path，设置默认 timeout，可扩展 headers/auth 等。
        """
        path = "/" + path.lstrip("/")
        url = f"{self.base_url}{path}"

        method = method.upper()
        # 取出headers, 并删除原来的headers
        headers = kwargs.pop("headers", {}) or {}
        #
        # 这里对headers进行处理
        #
        kwargs["headers"] = headers
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
