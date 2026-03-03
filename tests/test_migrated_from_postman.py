import pytest

from core.testdata import load_json_cases

from config.env import TOKEN

CASES = load_json_cases("data/postman_migrated_cases.json")

# @pytest.fixture(scope="session")
# def client():
#     return HttpClient(BASE_URL)


def _assert_keys(obj: dict, keys: list[str]):
    for k in keys:
        assert k in obj, f"missing key: {k}"


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["name"])
def test_migrated_cases(client, case):
    # headers = {"Accept": "application/json"}
    headers = {}
    if case.get("send_auth"):
        # 模拟 Postman 的 Authorization: Bearer {{token}}
        headers["Authorization"] = f"Bearer {TOKEN}"

    r = client.get(case["path"], headers=headers)

    # 1) 状态码断言（支持两种写法）
    if "expect_status" in case:
        assert r.status_code == case["expect_status"]
    if "expect_status_lt" in case:
        assert r.status_code < case["expect_status_lt"]

    # 2) JSON 结构断言（可选）
    if case.get("expect_array"):
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 0
        if "assert_json_keys" in case:
            _assert_keys(data[0], case["assert_json_keys"])
    elif "assert_json_keys" in case and r.status_code == 200:
        data = r.json()
        assert isinstance(data, dict)
        _assert_keys(data, case["assert_json_keys"])
