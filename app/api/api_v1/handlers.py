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


@v1_router.put(path="/welders/{id}")
def create_welder(id, welder_data: WelderShema) -> WelderShema:
    repo = WelderRepository()
    try:
        repo.add(welder_data)

        welder = repo.get(id)

        if not welder:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="welder not found after appending"
            )
        
        return welder
    
    except: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="welder not appended"
        )


@v1_router.patch(path="/welders/{id}")
def update_welder(id: str | int, welder_data: WelderShema) -> WelderShema:
    repo = WelderRepository()

    try:
        repo.update(id, **welder_data.model_dump(exclude_unset=True))

        welder = repo.get(id)

        if not welder:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="welder not found"
            )

        return welder
    
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="welder not updated"
        )


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


@v1_router.put(path="/welder-certifications/{id}")
def create_welder_certification(id, certification_data: WelderCertificationShema) -> WelderCertificationShema:
    repo = WelderCertificationRepository()
    try:
        repo.add(certification_data)

        certification = repo.get(id)

        if not certification:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="certification not found after appending"
            )
        
        return certification
    
    except: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="certification not appended"
        )


@v1_router.patch(path="/welder-certifications/{id}")
def update_welder_certification(id: str | int, certification_data: WelderCertificationShema) -> WelderCertificationShema:
    repo = WelderCertificationRepository()

    try:
        repo.update(id, **certification_data.model_dump(exclude_unset=True))

        certification = repo.get(id)

        if not certification:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="certification not found"
            )

        return certification
    
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="certification not updated"
        )


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


@v1_router.put(path="/ndts/{id}")
def create_ndt(id, ndt_data: WelderNDTShema) -> WelderNDTShema:
    repo = WelderNDTRepository()
    try:
        repo.add(ndt_data)

        ndt = repo.get(id)

        if not ndt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ndt not found after appending"
            )
        
        return ndt
    
    except: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ndt not appended"
        )


@v1_router.patch(path="/ndts/{id}")
def update_ndt(id: str | int, ndt_data: WelderNDTShema) -> WelderNDTShema:
    repo = WelderNDTRepository()

    try:
        repo.update(id, **ndt_data.model_dump(exclude_unset=True))

        ndt = repo.get(id)

        if not ndt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ndt not found"
            )

        return ndt
    
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ndt not updated"
        )


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
