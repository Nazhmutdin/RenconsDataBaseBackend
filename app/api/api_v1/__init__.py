from fastapi import APIRouter

from .welder_endpoints import welder_router
from .welder_certification_endpoints import welder_certification_router
from .welder_ndt_endpoint import welder_ndt_router

v1_router = APIRouter()

v1_router.include_router(router=welder_router, prefix="/welders")
v1_router.include_router(router=welder_certification_router, prefix="/welder-certifications")
v1_router.include_router(router=welder_ndt_router, prefix="/welder-ndts")
