#!/bin/bash
set -e

# Use virtual environment python/uvicorn if available
if [ -d "venv" ]; then
    PYTHON="./venv/bin/python3"
    UVICORN="./venv/bin/uvicorn"
else
    PYTHON="python3"
    UVICORN="uvicorn"
fi

echo "Starting Core Banking System (CBS) Mock FastAPI Server..."
echo "Swagger UI:  http://localhost:8000/docs"
echo "ReDoc UI:    http://localhost:8000/redoc"
echo "Healthcheck: http://localhost:8000/health"
echo "Log file:    logs/mock_server.log"

$UVICORN app.main:app --host 0.0.0.0 --port 8000 --reload
