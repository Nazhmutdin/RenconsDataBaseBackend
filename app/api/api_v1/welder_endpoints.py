from datetime import date

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.shemas import WelderShema
from app.utils.db_objects import DBResponse, WelderDataBaseRequest
from app.api.api_v1.depends import set_welder_database_request
from app.repositories import WelderRepository


welder_router = APIRouter()


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
def get_welders(request: WelderDataBaseRequest = Depends(set_welder_database_request)):
    repo = WelderRepository()
    # print(request)

    return repo.get_many(request)
