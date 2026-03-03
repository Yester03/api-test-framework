# api-test-framework

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Postman Collection (Day3)

- Import: `docs/postman/postman_collection_day3.json`
- Import env: `docs/postman/postman_environment_dev.json`
- Select env: `api-test-dev`
- Run: Collection Runner → verify all assertions pass

![postman](img/postman_result.png)
