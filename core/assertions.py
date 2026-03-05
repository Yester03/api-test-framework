# core/assertions.py
from __future__ import annotations
from typing import Any, Iterable, Mapping
import requests


# day10之前的断言封装
def assert_post_schema(data: dict, post_id: int):
    assert isinstance(data, dict)
    assert data["id"] == post_id
    assert isinstance(data.get("userId"), int)
    assert isinstance(data.get("title"), str)
    assert isinstance(data.get("body"), str)
    assert data["title"].strip() != ""
    assert data["body"].strip() != ""


# day10的断言封装


# 对接口返回的text进行截断
def _safe_text(resp: requests.Response, limit: int = 500) -> str:
    text = resp.text or ""
    return text[:limit] + ("..." if len(text) > limit else "")


# 对接口返回的不合法json进行错误提示
def _safe_json(resp: requests.Response):
    try:
        return resp.json()
    except Exception:
        assert False, (
            f"response is not valid JSON, url={resp.url}, status={resp.status_code}, body={_safe_text(resp)}"
        )


def assert_status(resp: requests.Response, expected: int) -> None:
    actual = resp.status_code
    assert actual == expected, (
        f"status_code expected={expected}, actual={actual}, url={resp.url}, body={_safe_text(resp)}"
    )


def assert_status_in(resp: requests.Response, expected_set: set[int]) -> None:
    actual = resp.status_code
    assert actual in expected_set, (
        f"status_code expected one of {sorted(expected_set)}, actual={actual}, url={resp.url}, body={_safe_text(resp)}"
    )


def assert_json_has_keys(resp: requests.Response, keys: Iterable[str]) -> None:
    data = _safe_json(resp)
    assert isinstance(data, Mapping), (
        f"json is not an object, url={resp.url}, json={data}"
    )

    missing = [k for k in keys if k not in data]
    assert not missing, f"missing keys={missing}, url={resp.url}, json={data}"


def assert_json_value(resp: requests.Response, key: str, expected: Any) -> None:
    data = _safe_json(resp)
    assert isinstance(data, Mapping), (
        f"json is not an object, url={resp.url}, json={data}"
    )

    actual = data.get(key, None)
    assert actual == expected, (
        f"json[{key}] expected={expected}, actual={actual}, url={resp.url}, json={data}"
    )


def assert_json_path_value(
    resp: requests.Response, path: str, expected: Any, sep: str = "."
) -> None:
    """
    path 示例：'data.user.id'（用于嵌套 JSON）
    """
    data = _safe_json(resp)
    cur: Any = data

    for part in path.split(sep):
        if isinstance(cur, Mapping) and part in cur:
            cur = cur[part]
        else:
            assert False, (
                f"path not found: {path}, stopped_at={part}, url={resp.url}, json={data}"
            )

    assert cur == expected, (
        f"path({path}) expected={expected}, actual={cur}, url={resp.url}, json={data}"
    )
