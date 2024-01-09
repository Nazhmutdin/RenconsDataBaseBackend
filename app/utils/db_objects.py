from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator, Field
from app.utils.funcs import str_to_date

from app.utils.base_shema import BaseShema


class BaseRequest(BaseModel):
    limit: int = Field(default=100)
    offset: int = Field(default=0)


class WelderCertificationRequest(BaseRequest):
    kleymos: list[str] = Field(default=[])
    ids: list[str] = Field(default=[])
    certification_numbers: list[str] = Field(default=[], alias="certificationNumbers")
    certification_date_from: date | None = Field(default=None, alias="certificationDateFrom")
    certification_date_before: date | None = Field(default=None, alias="certificationDateBefore")
    expiration_date_from: date | None = Field(default=None, alias="expirationDateFrom")
    expiration_date_before: date | None = Field(default=None, alias="expirationDateBefore")
    expiration_date_fact_from: date | None = Field(default=None, alias="expirationDateFactFrom")
    expiration_date_fact_before: date | None = Field(default=None, alias="expirationDateFactBefore")
    details_thikness_from: float | None = Field(default=None, alias="detailsThiknessFrom")
    details_thikness_before: float | None = Field(default=None, alias="detailsThiknessBefore")
    outer_diameter_from: float | None = Field(default=None, alias="outerDiameterFrom")
    outer_diameter_before: float | None = Field(default=None, alias="outerDiameterBefore")
    rod_diameter_from: float | None = Field(default=None, alias="rodDiameterFrom")
    rod_diameter_before: float | None = Field(default=None, alias="rodDiameterBefore")
    details_diameter_from: float | None = Field(default=None, alias="detailsDiameterFrom")
    details_diameter_before: float | None = Field(default=None, alias="detailsDiameterBefore")
    gtd: list[str] = Field(default=[])
    method: list[str] = Field(default=[])


class WelderRequest(BaseRequest):
    names: list[str] | None = Field(default=None)
    kleymos: list[str] | None = Field(default=None)
    certification_numbers: list[str] | None = Field(default=None, alias="certificationNumbers")
    expiration_date_fact_from: date | str | None = Field(default=None, alias="expirationDateFactFrom")
    expiration_date_fact_before: date | str | None = Field(default=None, alias="expirationDateFactBefore")
    expiration_date_from: date | str | None = Field(default=None, alias="expirationDateFrom")
    expiration_date_before: date | str | None = Field(default=None, alias="expirationDateBefore")
    certification_date_from: date | str | None = Field(default=None, alias="certificationDateFrom")
    certification_date_before: date | str | None = Field(default=None, alias="certificationDateBefore")
    status: int | None = Field(default=None)

    model_config = ConfigDict(
        populate_by_name = True
    )

    @field_validator(
        "expiration_date_fact_from",
        "expiration_date_fact_before",
        "expiration_date_from", 
        "expiration_date_before", 
        "certification_date_from", 
        "certification_date_before"
    )
    @classmethod
    def validate_date(cls, v) -> date | None:
        if type(v) == date:
            return v
        
        if type(v) == str:
            v = str_to_date(v)

            if type(v) == date:
                return v
            
            return None
        
        if v == None:
            return None
        

    @field_validator(
        "names",
        "kleymos",
        "certification_numbers"
    )
    @classmethod
    def validate_list(cls, v: list | None) -> list | None:
        if v == None:
            return None
        
        if len(v) == 1 and v[0] == "":
            return None
        
        return v


class WelderNDTRequest(BaseRequest):    
    names: list[str] | None = Field(default=None)
    kleymos: list[str | int] | None = Field(default=None)
    comps: list[str] | None = Field(default=None)
    subcomps: list[str] | None = Field(default=None)
    projects: list[str] | None = Field(default=None)
    welding_date_from: date | str | None = Field(default=None, alias="weldingDateFrom")
    welding_date_before: date | str | None = Field(default=None, alias="weldingDateBefore")
    status_1_from: str | int | float | None = Field(default=None, alias="status1From")
    status_1_before: str | int | float | None = Field(default=None, alias="status1Before")
    status_2_from: str | int | float | None = Field(default=None, alias="status2From")
    status_2_before: str | int | float | None = Field(default=None, alias="status2Before")
    status_3_from: str | int | float | None = Field(default=None, alias="status3From")
    status_3_before: str | int | float | None = Field(default=None, alias="status3Before")


    @field_validator(
        "welding_date_from",
        "welding_date_before"
    )
    @classmethod
    def validate_date(cls, v) -> date | None:
        if type(v) == date:
            return v
        
        if type(v) == str:
            v = str_to_date(v)

            if type(v) == date:
                return v
            
            return None
        
        if v == None:
            return None


class DBResponse[Model:BaseShema](BaseModel):
    count: int
    result: list[Model]
