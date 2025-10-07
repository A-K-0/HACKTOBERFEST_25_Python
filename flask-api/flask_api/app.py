#!/usr/bin/env python3
"""
Simple Flask API

Endpoints:
- GET  /                 -> Welcome + list available endpoints
- GET  /health           -> Basic health check
- GET  /echo             -> Echo back query params and (optional) JSON body
- GET  /add              -> a + b (query params: a, b)
- GET  /random           -> random int in [low, high] (query: low, high)
- POST /compute/power    -> JSON body {"base": number, "exp": number}

Run:
    pip install Flask
    python projects/flask_api/app.py

The API listens on http://127.0.0.1:5000 by default.
"""
from __future__ import annotations
import os
import random
from datetime import datetime, timezone
from typing import Any, Dict

from flask import Flask, jsonify, request

app = Flask(__name__)


def _error(message: str, status: int = 400):
    resp = jsonify({"error": message, "status": status})
    resp.status_code = status
    return resp


@app.get("/")
def index():
    return jsonify(
        {
            "message": "Welcome to the Simple Flask API",
            "endpoints": {
                "health": {"method": "GET", "path": "/health"},
                "echo": {"method": "GET", "path": "/echo"},
                "add": {"method": "GET", "path": "/add", "query": ["a", "b"]},
                "random": {"method": "GET", "path": "/random", "query": ["low", "high"]},
                "compute_power": {"method": "POST", "path": "/compute/power", "json": {"base": "number", "exp": "number"}},
            },
        }
    )


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "time": datetime.now(timezone.utc).isoformat(),
            "service": "flask-api",
        }
    )


@app.get("/echo")
def echo():
    body = request.get_json(silent=True)
    return jsonify(
        {
            "query": request.args.to_dict(flat=True),
            "json": body,
        }
    )


@app.get("/add")
def add():
    a = request.args.get("a")
    b = request.args.get("b")
    if a is None or b is None:
        return _error("Missing query parameters 'a' and/or 'b'", 400)
    try:
        a_val = float(a)
        b_val = float(b)
    except ValueError:
        return _error("Parameters 'a' and 'b' must be numbers", 400)
    return jsonify({"a": a_val, "b": b_val, "sum": a_val + b_val})


@app.get("/random")
def random_int():
    low = request.args.get("low")
    high = request.args.get("high")
    if low is None or high is None:
        return _error("Missing query parameters 'low' and/or 'high'", 400)
    try:
        low_i = int(low)
        high_i = int(high)
    except ValueError:
        return _error("Parameters 'low' and 'high' must be integers", 400)
    if low_i > high_i:
        return _error("'low' must be <= 'high'", 400)
    value = random.randint(low_i, high_i)
    return jsonify({"low": low_i, "high": high_i, "value": value})


@app.post("/compute/power")
def compute_power():
    body = request.get_json(silent=False)
    if not isinstance(body, dict):
        return _error("JSON body must be an object", 400)
    if "base" not in body or "exp" not in body:
        return _error("JSON must include 'base' and 'exp'", 400)
    try:
        base = float(body["base"])  # allow ints/floats
        exp = float(body["exp"])
    except (TypeError, ValueError):
        return _error("'base' and 'exp' must be numbers", 400)
    return jsonify({"base": base, "exp": exp, "result": base ** exp})


# JSON error handlers
@app.errorhandler(404)
def not_found(_e):
    return _error("Not Found", 404)


@app.errorhandler(405)
def method_not_allowed(_e):
    return _error("Method Not Allowed", 405)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
