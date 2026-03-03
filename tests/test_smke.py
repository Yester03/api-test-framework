import requests


def test_health_check():
    r = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == 1
