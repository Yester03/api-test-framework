from core.http_client import HttpClient
from config.env import BASE_URL
from core.assertions import assert_post_schema
import requests
import pytest

# 创建client
client = HttpClient(BASE_URL)


@pytest.mark.parametrize(
    "post_id, expected_status",
    [
        (1, 200),
        (2, 200),
        (100, 200),
    ],
)
def test_get_post_happy(post_id, expected_status):
    # r = requests.get(f"{BASE_URL}/posts/{post_id}", timeout=10)
    r = client.get(f"/posts/{post_id}")
    assert r.status_code == expected_status
    data = r.json()
    # assert data["id"] == post_id
    # assert "title" in data and "body" in data and "userId" in data
    assert_post_schema(data, post_id)
