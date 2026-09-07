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

echo "=========================================================="
echo " Starting Bharat Bank Multi-Server Architecture"
echo "=========================================================="
echo " 1. Core Banking System (CBS) Mock Server:  http://localhost:8000/docs"
echo " 2. Omnichannel Digital Backend Server:     http://localhost:8080/docs"
echo "=========================================================="

# Trap SIGINT and SIGTERM to kill background processes on exit
trap 'kill $(jobs -p)' EXIT

# Start CBS Server in background
$UVICORN app.main:app --host 0.0.0.0 --port 8000 &
CBS_PID=$!

# Start Digital Backend Server in background
$UVICORN digital_backend.main:app --host 0.0.0.0 --port 8080 &
DIGITAL_PID=$!

wait $CBS_PID $DIGITAL_PID
