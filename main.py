from fastapi import FastAPI

from app.api.api_v1 import v1_router

app = FastAPI()

app.include_router(router=v1_router, prefix="/api/v1")
