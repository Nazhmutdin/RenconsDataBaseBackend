from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status

from app.shemas import WelderNDTShema, WelderShema, WelderCertificationShema
from app.repositories import WelderNDTRepository, WelderRepository, WelderCertificationRepository
from app.utils.db_objects import DBResponse, WelderNDTRequest, WelderRequest, WelderCertificationRequest
from app.api.api_v1.depends import set_welder_ndt_request, set_welder_request, set_welder_certification_request


v1_router = APIRouter()


@v1_router.get(path="/welders/{id}")
def get_welder(id: str | int) -> WelderShema:
    repo = WelderRepository()

    res = repo.get(id)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="welder not found"
        )
    
    return res


@v1_router.put(path="/welders")
def add_welder(welder_data: WelderShema) -> WelderShema:
    repo = WelderRepository()
    welder = repo.get(welder_data.kleymo)

    if welder:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="welder already exist"
        )

    repo.add(welder_data)

    return welder_data


@v1_router.patch(path="/welders")
def update_welder(welder_data: WelderShema) -> WelderShema:
    repo = WelderRepository()

    welder = repo.get(welder_data.kleymo)

    if not welder:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="welder not found"
        )
    
    repo.update(welder_data.kleymo, **welder_data.model_dump(exclude_unset=True))
    
    return welder.update(**welder_data.model_dump(exclude_unset=True))


@v1_router.delete(path="/welders/{id}")
def delete_welder(id: str | int) -> WelderShema:
    repo = WelderRepository()
    welder = repo.get(id)

    if not welder:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="welder not found"
        )

    repo.delete(id)

    return welder


@v1_router.post(path="/welders", response_model=DBResponse[WelderShema])
def get_welders(request: Annotated[WelderRequest, Depends(set_welder_request)]):
    repo = WelderRepository()

    return repo.get_many(request)


"""
=================================================================================================
welder certification routes
=================================================================================================
"""


@v1_router.get(path="/welder-certifications/{id}")
def get_welder_certification(id: str) -> WelderCertificationShema | None:
    repo = WelderCertificationRepository()

    res = repo.get(id)

    if not res:
        return {
            "result": res
        }
    
    return res


@v1_router.put(path="/welder-certifications")
def add_welder_certification(certification_data: WelderCertificationShema) -> WelderCertificationShema:
    repo = WelderCertificationRepository()
    certification = repo.get(certification_data.certification_id)

    if certification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="certification already exist"
        )

    repo.add(certification_data)
    
    return certification_data


@v1_router.patch(path="/welder-certifications")
def update_welder_certification(certification_data: WelderCertificationShema) -> WelderCertificationShema:
    repo = WelderCertificationRepository()
    certification = repo.get(certification_data.certification_id)

    if not certification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="certification not found"
        )

    repo.update(certification_data.certification_id, **certification_data.model_dump(exclude_unset=True))

    return certification.update(**certification_data.model_dump(exclude_unset=True))


@v1_router.delete(path="/welder-certifications/{id}")
def delete_welder_certification(id: str | int) -> WelderCertificationShema:
    repo = WelderCertificationRepository()
    certification = repo.get(id)

    if not certification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="certification not found"
        )
    
    repo.delete(id)

    return certification


@v1_router.post(path="/welder-certifications", response_model=DBResponse[WelderCertificationShema])
def get_welder_certifications(request: Annotated[WelderCertificationRequest, Depends(set_welder_certification_request)]):
    repo = WelderCertificationRepository()

    return repo.get_many(request)


"""
=================================================================================================
ndt routes
=================================================================================================
"""


@v1_router.get(path="/ndts/{id}")
def get_ndt(id) -> WelderNDTShema:
    repo = WelderNDTRepository()

    ndt = repo.get(id)

    if not ndt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ndt not found"
        )
    
    return ndt


@v1_router.put(path="/ndts")
def add_ndt(ndt_data: WelderNDTShema) -> WelderNDTShema:
    repo = WelderNDTRepository()
    ndt = repo.get(ndt_data.ndt_id)

    if ndt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ndt already exist"
        )
    
    repo.add(ndt_data)
    
    return ndt_data


@v1_router.patch(path="/ndts")
def update_ndt(ndt_data: WelderNDTShema) -> WelderNDTShema:
    repo = WelderNDTRepository()

    ndt = repo.get(ndt_data.ndt_id)

    if not ndt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ndt not found"
        )
        
    repo.update(ndt_data.ndt_id, **ndt_data.model_dump(exclude_unset=True))

    return ndt.update(**ndt_data.model_dump(exclude_unset=True))


@v1_router.delete(path="/ndts/{id}")
def delete_ndt(id: str | int) -> WelderNDTShema:
    repo = WelderNDTRepository()
    ndt = repo.get(id)

    if not ndt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ndt not found"
        )
    
    repo.delete(id)

    return ndt


@v1_router.post(path="/ndts", response_model=DBResponse[WelderNDTShema])
def get_ndts(request: Annotated[WelderNDTRequest, Depends(set_welder_ndt_request)]):
    repo = WelderNDTRepository()

    return repo.get_many(request)
