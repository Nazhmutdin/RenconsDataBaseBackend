from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator, Field

from app.utils.db_objects import WelderDataBaseRequest
from app.utils.funcs import str_to_date


class WelderHTTPRequest(BaseModel):
    names: list[str] = Field(default=[])
    kleymos: list[str] = Field(default=[])
    certification_numbers: list[str] = Field(default=[], alias="certificationNumbers")
    expiration_date_fact_from: date | str | None = Field(default=None, alias="expirationDateFactFrom")
    expiration_date_fact_before: date | str | None = Field(default=None, alias="expirationDateFactBefore")
    expiration_date_from: date | str | None = Field(default=None, alias="expirationDateFrom")
    expiration_date_before: date | str | None = Field(default=None, alias="expirationDateBefore")
    certification_date_from: date | str | None = Field(default=None, alias="certificationDateFrom")
    certification_date_before: date | str | None = Field(default=None, alias="certificationDateBefore")

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
    def validate_list(cls, v: list) -> list:
        if len(v) == 1 and v[0] == "":
            print(v)
            return []
        
        return v


def set_welder_database_request(http_request: WelderHTTPRequest = WelderHTTPRequest(), page: int = 1, page_size: int = 100) -> WelderDataBaseRequest:
    
    print(http_request)

    if page < 1:
        page = 1
    
    if page_size < 1:
        page_size = 100

    return WelderDataBaseRequest(
        **http_request.model_dump(),
        limit=page_size,
        offset=(page - 1) * page_size
    )
