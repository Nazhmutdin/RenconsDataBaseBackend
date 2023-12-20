from fastapi import APIRouter, Depends

from app.shemas import WelderCertificationShema
from app.repositories import WelderCertificationRepository
from app.utils.db_objects import DBResponse, WelderCertificationDataBaseRequest
from app.api.api_v1.depends import set_welder_certification_database_request


welder_certification_router = APIRouter()


@welder_certification_router.get(path="/{id}")
def get_welder_certification(id: str) -> WelderCertificationShema | None:
    repo = WelderCertificationRepository()

    res = repo.get(id)

    if res != None:
        return res
    
    return {
        "result": res
    }


@welder_certification_router.post(path="/",response_model=DBResponse[WelderCertificationShema])
def get_welders(request: WelderCertificationDataBaseRequest = Depends(set_welder_certification_database_request)):
    repo = WelderCertificationRepository()

    return repo.get_many(request)
