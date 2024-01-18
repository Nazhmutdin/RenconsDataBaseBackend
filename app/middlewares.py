from typing import Any, Coroutine, Callable, Awaitable
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from starlette.types import Message

from app.repositories import UserRepository
from app.api.auth.utils import Token, read_token, verify_password


class CheckAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app=app)

    
    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    
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
            token_data = read_token(Token(access_token=token))
        except:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid token"}
            )
        
        user = UserRepository().get(token_data.login)

        if not user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "User not found"}
            )

        if not verify_password(token_data.password, user.hashed_password):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid password"}
            )
        
        return await call_next(request)
