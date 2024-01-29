import typing

from pydantic import BaseModel as BaseDomainModel

from app.db_engine import BaseModel


_Shema = typing.TypeVar("_Shema", bound="BaseShema")


class BaseShema[Model: BaseModel](BaseDomainModel):
    __table_model__: Model

    def __eq__(self, __value: BaseModel) -> bool:
        if not isinstance(__value, type(self)):
            return False
        
        self_dict = self.model_dump()

        for key, value in __value.model_dump().items():
            if key not in self_dict:
                return False
            
            if value != self_dict[key]:
                return False
        
        return True
    

    def update(self, **kwargs) -> typing.Self:
        for key, value in kwargs.items():
            setattr(self, key, value)

        return self
