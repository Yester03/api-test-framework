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

## Day4 - Migrate Postman Collection to Pytest (Data-driven)

This project migrates a Postman collection (10+ requests) into a pytest-based API automation suite.

### What’s included

- Data-driven test cases (`data/postman_migrated_cases.json`)
- Reusable HTTP client (`core/http_client.py`)
- Environment-based configuration (`config/env.py`)
- One-command run: `python -m pytest -q`

### Run (Windows PowerShell)

```powershell
# optional: override environment variables
$env:BASE_URL="https://jsonplaceholder.typicode.com"
$env:TOKEN="fake_token_123"
$env:TIMEOUT="10"

python -m pytest -q
```