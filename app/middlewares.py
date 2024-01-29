from typing import Any, Coroutine, Callable, Awaitable
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse

from app.api.auth.utils import Token, read_token, get_user


class CheckAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app=app)

    
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Coroutine[Any, Any, Response]:

        if "/api/v1" not in request.url.path:
            return await call_next(request)
        
        try:
            token: str = request.cookies.get("access_token", None)
        except:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "detail": "body is invalid"
                }
            )

        if token == None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "token is required"}
            )

        try:
            read_token(Token(access_token=token))
        except:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid token"}
            )
        
        return await call_next(request)
