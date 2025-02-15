from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os

SECURE_DATA_DIR = os.path.abspath("./data")

class EnforceDataAccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        requested_path = request.url.path
        if not requested_path.startswith("/data"):
            raise HTTPException(status_code=403, detail="Access outside /data is not allowed")
        return await call_next(request)