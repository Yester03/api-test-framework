# core/http_client.py
from __future__ import annotations
import requests


class HttpClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, path: str, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.session.get(url, timeout=self.timeout, **kwargs)
