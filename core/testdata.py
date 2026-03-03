import json
from pathlib import Path


def load_json_cases(path: str):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))
