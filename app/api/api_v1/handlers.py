from typing import Annotated

from fastapi import APIRouter, Depends

from app.shemas import WelderNDTShema, WelderShema, WelderCertificationShema
from app.repositories import WelderNDTRepository, WelderRepository, WelderCertificationRepository
from app.utils.db_objects import DBResponse, WelderNDTRequest, WelderRequest, WelderCertificationRequest
from app.api.api_v1.depends import set_welder_ndt_request, set_welder_request, set_welder_certification_request


v1_router = APIRouter()


@v1_router.get(path="/welder-ndts/{id}")
def get_ndt(id) -> WelderNDTShema | dict:
    repo = WelderNDTRepository()

    ndt = repo.get(id)

    if ndt == None:
        return {
            "result": "ndt not found"
        }
    
    return ndt


@v1_router.post(path="/welder-ndts/", response_model=DBResponse[WelderNDTShema])
def get_ndts(request: Annotated[WelderNDTRequest, Depends(set_welder_ndt_request)]):
    repo = WelderNDTRepository()

    return repo.get_many(request)


@v1_router.get(path="/welders/{id}")
def get_welder(id: str | int) -> WelderShema | dict[str, str]:
    repo = WelderRepository()

    res = repo.get(id)

    if res != None:
        return res
    
    return {
        "result": "welder not found"
    }


@v1_router.post(path="/welders/", response_model=DBResponse[WelderShema])
def get_welders(request: Annotated[WelderRequest, Depends(set_welder_request)]):
    repo = WelderRepository()

    return repo.get_many(request)



@v1_router.get(path="/welder-certifications/{id}")
def get_welder_certification(id: str) -> WelderCertificationShema | None:
    repo = WelderCertificationRepository()

    res = repo.get(id)

    if res != None:
        return res
    
    return {
        "result": res
    }


@v1_router.post(path="/welder-certifications/", response_model=DBResponse[WelderCertificationShema])
def get_welders(request: Annotated[WelderCertificationRequest, Depends(set_welder_certification_request)]):
    repo = WelderCertificationRepository()

    return repo.get_many(request)
