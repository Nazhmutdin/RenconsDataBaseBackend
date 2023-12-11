import typing

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from pydantic import BaseModel

from app.settings import Settings



DB_URL = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
    Settings.USER(), 
    Settings.DB_PASSWORD(), 
    Settings.HOST(), 
    Settings.PORT(), 
    Settings.DB_NAME()
)


class BaseModel(DeclarativeBase): ...


engine = create_engine(DB_URL)

BaseModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
