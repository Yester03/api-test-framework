# core/assertions.py
def assert_post_schema(data: dict, post_id: int):
    assert isinstance(data, dict)
    assert data["id"] == post_id
    assert isinstance(data.get("userId"), int)
    assert isinstance(data.get("title"), str)
    assert isinstance(data.get("body"), str)
    assert data["title"].strip() != ""
    assert data["body"].strip() != ""
