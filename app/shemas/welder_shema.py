from datetime import date
from re import fullmatch

from pydantic import Field, field_validator

from app.models import WelderModel
from app.utils.base_shema import BaseShema
from app.shemas.welder_certification_shema import WelderCertificationShema


class WelderShema(BaseShema):
    __table_model__ = WelderModel
    kleymo: str = Field(default="")
    name: str | None  = Field(default=None)
    birthday: date | None  = Field(default=None)
    passport_id: str | None = Field(default=None)
    sicil_number: str | None = Field(default=None)
    nation: str | None = Field(default=None)
    status: int = Field(default=0)


    @field_validator("kleymo")
    def validate_kleymo(cls, v: str):
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")
