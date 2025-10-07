# Simple Flask API

A minimal Flask API exposing a few beginner-friendly endpoints.

- **Language**: Python 3.8+
- **Files**:
  - `projects/flask_api/app.py` (application)
  - `projects/flask_api/README.md` (this file)

## Setup
```bash
# Optionally create and activate a virtual environment
# python -m venv .venv
# .venv\Scripts\activate   # Windows PowerShell

pip install Flask
```

## Run
```bash
python projects/flask_api/app.py
# Server: http://127.0.0.1:5000
```

## Endpoints
- **GET /**
  - Welcome + list endpoints

- **GET /health**
  - Basic health check with UTC timestamp

- **GET /echo**
  - Echos query params and optional JSON body
  - Example:
    ```bash
    curl "http://127.0.0.1:5000/echo?name=Mohan"
    ```

- **GET /add?a=NUMBER&b=NUMBER**
  - Returns sum
  - Example:
    ```bash
    curl "http://127.0.0.1:5000/add?a=2&b=3"
    ```

- **GET /random?low=INT&high=INT**
  - Random integer between [low, high]
  - Example:
    ```bash
    curl "http://127.0.0.1:5000/random?low=1&high=10"
    ```

- **POST /compute/power**
  - JSON: {"base": number, "exp": number}
  - Example:
    ```bash
    curl -X POST http://127.0.0.1:5000/compute/power \
      -H "Content-Type: application/json" \
      -d '{"base": 2, "exp": 8}'
    ```

## Notes
- No database, no auth — purely for learning.
- You can change the port by setting `PORT` env var before running.
