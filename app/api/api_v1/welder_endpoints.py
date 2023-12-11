from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.shemas import WelderShema
from app.utils.db_objects import DBResponse, WelderDataBaseRequest
from app.repositories import WelderRepository


welder_router = APIRouter()


class WelderHTTPRequest(BaseModel):
    names: list[str] | None = Field(default=None)
    kleymos: list[str | int] | None = Field(default=None)
    certification_numbers: list[str] | None = Field(default=None)


@welder_router.get(path="/{id}")
def get_welder(id: str | int):
    repo = WelderRepository()

    res = repo.get(id)

    if res != None:
        return res
    
    return {
        "result": res
    }


@welder_router.post(path="/",response_model=DBResponse[WelderShema])
def get_welders(request: WelderHTTPRequest = WelderHTTPRequest(), page: int = 1, page_size: int = 100):
    repo = WelderRepository()

    if page < 1:
        page = 1
    
    if page_size < 1:
        page_size = 100


    request = WelderDataBaseRequest(
        **request.model_dump(),
        limit=page_size,
        offset=(page - 1) * page_size
    )

    return repo.get_many(request)
