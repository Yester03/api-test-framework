# core/http_client.py
from __future__ import annotations

from typing import Mapping
import requests


class HttpClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        default_headers: Mapping[str, str] | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.default_headers = dict(default_headers or {})

    def _merge_headers(self, headers: Mapping[str, str] | None) -> dict[str, str]:
        merged = dict(self.default_headers)
        if headers:
            merged.update(headers)  # request-level headers override defaults
        return merged

    def get(self, path: str, headers: Mapping[str, str] | None = None, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = self._merge_headers(headers)
        return self.session.get(
            url, timeout=self.timeout, headers=final_headers, **kwargs
        )
