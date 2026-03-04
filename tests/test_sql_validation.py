import sqlite3
import requests
from pathlib import Path

DB_PATH = Path("reports/demo.db")
BASE_URL = "https://jsonplaceholder.typicode.com"


def test_posts_count_matches_expected():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM posts;")
    (cnt,) = cur.fetchone()
    conn.close()

    assert cnt == 100


def test_posts_count_api_equals_db():
    api_cnt = len(requests.get(f"{BASE_URL}/posts", timeout=10).json())
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM posts;")
    (db_cnt,) = cur.fetchone()
    conn.close()

    assert api_cnt == db_cnt
