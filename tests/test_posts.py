# import requests
import pytest
from core.client import APIClient
from core.assertions import (
    assert_status,
    assert_status_in,
    assert_json_has_keys,
    assert_json_value,
    assert_json_path_value,
)
# BASE_URL = "https://jsonplaceholder.typicode.com"

# 使用统一client进行接口请求
client = APIClient()


# 最简单的测试单元
def test_get_post_1():
    # url = f"{BASE_URL}/posts/1"

    # r = requests.get(url)

    r = client.get("/posts/1")

    # assert r.status_code == 200
    # assert r.json()["id"] == 1
    assert_status(r, 200)
    assert_json_value(r, "id", 1)


# 参数化测试
@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_post(post_id):
    # url = f"{BASE_URL}/posts/{post_id}"
    # r = requests.get(url)

    r = client.get(f"/posts/{post_id}")

    # assert r.status_code == 200
    # assert r.json()["id"] == post_id

    # 使用封装的assertioner写断言
    assert_status(r, 200)
    assert_json_value(r, "id", post_id)
    assert_json_has_keys(r, ["userId", "title", "body"])


# 测试帖子总数不为空
def test_posts_list():
    # r = requests.get(f"{BASE_URL}/posts")
    r = client.get("/posts")

    # assert r.status_code == 200
    assert_status(r, 200)
    assert isinstance(r.json(), list)
    assert len(r.json()) > 0


# 测试很大的id, 可以成功, 也可以失败
def test_invalid_post():
    # r = requests.get(f"{BASE_URL}/posts/999999")
    r = client.get("/posts/999999")

    # assert r.status_code in [200, 404]
    assert_status_in(r, {200, 404})


# 测试必要字段是否存在
def test_post_structure():
    # r = requests.get(f"{BASE_URL}/posts/1")
    r = client.get("/posts/1")

    # data = r.json()
    # assert r.status_code == 200
    # assert "userId" in data
    # assert "title" in data
    # assert "body" in data
    assert_status(r, 200)
    assert_json_has_keys(r, ["userId", "title", "body"])
