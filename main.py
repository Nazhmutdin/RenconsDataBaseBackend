from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1 import v1_router
from app.api.auth.auth_endpoints import auth_router

app = FastAPI()


origins = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://10.10.116.200:8080"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods"
    ],
)

app.include_router(router=v1_router, prefix="/api/v1")
app.include_router(router=auth_router, prefix="")
