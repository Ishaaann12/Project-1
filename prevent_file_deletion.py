from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class PreventFileDeletionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method.upper() == "DELETE":
            raise HTTPException(status_code=403, detail="File deletions are not allowed")
        return await call_next(request)