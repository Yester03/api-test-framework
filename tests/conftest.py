import pytest

from core.http_client import HttpClient
from config.env import BASE_URL
from config.env import TIMEOUT


@pytest.fixture(scope="session")
def client():
    return HttpClient(
        BASE_URL,
        timeout=TIMEOUT,
        default_headers={"Accept": "application/json"},
    )
