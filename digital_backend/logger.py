import logging
import os
import sys
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from digital_backend.config import settings

os.makedirs(os.path.dirname(settings.log_file_path), exist_ok=True)

logger = logging.getLogger("digital_backend")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] [DIGITAL-BACKEND] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if settings.log_to_file:
        file_handler = logging.FileHandler(settings.log_file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        url = request.url.path

        response: Response = await call_next(request)
        process_time_ms = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"Client: {client_ip} | {method} {url} | Status: {response.status_code} | Duration: {process_time_ms}ms"
        )
        return response
