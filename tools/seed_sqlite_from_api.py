import sqlite3
import requests
from pathlib import Path

BASE_URL = "https://jsonplaceholder.typicode.com"
DB_PATH = Path("reports/demo.db")


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    posts = requests.get(f"{BASE_URL}/posts", timeout=10).json()
    users = requests.get(f"{BASE_URL}/users", timeout=10).json()
    comments = requests.get(f"{BASE_URL}/comments", timeout=10).json()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # drop & create
    cur.executescript("""
    DROP TABLE IF EXISTS posts;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS comments;

    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL
    );

    CREATE TABLE posts (
        id INTEGER PRIMARY KEY,
        userId INTEGER NOT NULL,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        FOREIGN KEY(userId) REFERENCES users(id)
    );

    CREATE TABLE comments (
        id INTEGER PRIMARY KEY,
        postId INTEGER NOT NULL,
        email TEXT,
        body TEXT,
        FOREIGN KEY(postId) REFERENCES posts(id)
    );
    """)

    cur.executemany(
        "INSERT INTO users(id, username) VALUES(?, ?)",
        [(u["id"], u["username"]) for u in users],
    )
    cur.executemany(
        "INSERT INTO posts(id, userId, title, body) VALUES(?, ?, ?, ?)",
        [(p["id"], p["userId"], p["title"], p["body"]) for p in posts],
    )
    cur.executemany(
        "INSERT INTO comments(id, postId, email, body) VALUES(?, ?, ?, ?)",
        [(c["id"], c["postId"], c["email"], c["body"]) for c in comments],
    )

    conn.commit()
    conn.close()
    print(f"Seeded sqlite db: {DB_PATH.resolve()}")


if __name__ == "__main__":
    main()
