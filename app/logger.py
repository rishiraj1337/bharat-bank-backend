import time
import os
import logging
from logging.handlers import RotatingFileHandler
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "mock_server.log")

# Setup root logger
logger = logging.getLogger("mock_cbs")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5, encoding="utf-8")
file_handler.setFormatter(console_formatter)
logger.addHandler(file_handler)


class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip logging for health checks or docs assets if desired
        path = request.url.path
        if path.startswith("/openapi.json") or path.startswith("/docs") or path.startswith("/redoc"):
            return await call_next(request)

        start_time = time.time()
        client_host = request.client.host if request.client else "unknown"
        
        # Read request body
        req_body_bytes = await request.body()
        req_body_str = req_body_bytes.decode("utf-8", errors="replace") if req_body_bytes else "<empty>"

        # Re-populate receive stream so downstream route handlers can read request.body()
        async def receive():
            return {"type": "http.request", "body": req_body_bytes, "more_body": False}
        request = Request(request.scope, receive=receive)

        # Log Incoming Request
        headers_dict = dict(request.headers)
        # Filter out verbose authorization/cookie headers if any exist
        req_summary = (
            f"\n>>> INCOMING REQUEST >>>\n"
            f"Method:  {request.method} {request.url}\n"
            f"Client:  {client_host}\n"
            f"Headers: {headers_dict}\n"
            f"Body:\n{req_body_str}\n"
        )
        logger.info(req_summary)

        # Execute request
        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = (time.time() - start_time) * 1000.0
            logger.error(f"!!! REQUEST FAILED: {request.method} {request.url} in {duration_ms:.2f}ms - Exception: {exc}", exc_info=True)
            raise

        # Capture response body
        resp_body = [section async for section in response.body_iterator]
        response.body_iterator = _iterate_in_chunks(resp_body)
        resp_body_bytes = b"".join(resp_body)
        resp_body_str = resp_body_bytes.decode("utf-8", errors="replace") if resp_body_bytes else "<empty>"

        duration_ms = (time.time() - start_time) * 1000.0

        # Log Outgoing Response
        resp_summary = (
            f"\n<<< OUTGOING RESPONSE <<<\n"
            f"Method:   {request.method} {request.url}\n"
            f"Status:   {response.status_code}\n"
            f"Duration: {duration_ms:.2f}ms\n"
            f"Headers:  {dict(response.headers)}\n"
            f"Body:\n{resp_body_str}\n"
        )
        logger.info(resp_summary)

        return response


async def _iterate_in_chunks(chunks):
    for chunk in chunks:
        yield chunk
