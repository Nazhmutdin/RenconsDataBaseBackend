from fastapi import APIRouter, Depends

from app.shemas import WelderNDTShema
from app.repositories import WelderNDTRepository
from app.utils.db_objects import DBResponse, WelderNDTDataBaseRequest
from app.api.api_v1.depends import set_welder_ndt_database_request


welder_ndt_router = APIRouter()


@welder_ndt_router.get(path="/{id}")
def get_ndt(id) -> WelderNDTShema | dict:
    repo = WelderNDTRepository()

    ndt = repo.get(id)

    if ndt == None:
        return {
            "result": "ndt not found"
        }
    
    return ndt


@welder_ndt_router.post(path="/", response_model=DBResponse[WelderNDTShema])
def get_ndts(request: WelderNDTDataBaseRequest = Depends(set_welder_ndt_database_request)):
    repo = WelderNDTRepository()

    return repo.get_many(request)
