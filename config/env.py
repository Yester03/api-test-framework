# config/env.py
import os

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")

TIMEOUT = int(os.getenv("TIMEOUT", "10"))

TOKEN = os.getenv("TOKEN", "fake_token_123")
