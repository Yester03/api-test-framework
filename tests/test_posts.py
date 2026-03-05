import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"


# 最简单的测试单元
def test_get_post_1():
    url = f"{BASE_URL}/posts/1"

    r = requests.get(url)

    assert r.status_code == 200
    assert r.json()["id"] == 1


# 参数化测试
@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"

    r = requests.get(url)

    assert r.status_code == 200
    assert r.json()["id"] == post_id


# 测试帖子不为空
def test_posts_list():
    r = requests.get(f"{BASE_URL}/posts")

    assert r.status_code == 200
    assert len(r.json()) > 0


# 测试很大的id, 可以成功, 也可以失败
def test_invalid_post():
    r = requests.get(f"{BASE_URL}/posts/999999")

    assert r.status_code in [200, 404]


# 测试必要字段是否存在
def test_post_structure():
    r = requests.get(f"{BASE_URL}/posts/1")

    data = r.json()

    assert "userId" in data
    assert "title" in data
    assert "body" in data
