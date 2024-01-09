import os

from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseModel):

    @classmethod
    def DB_NAME(cls) -> str:
        return os.getenv("DATABASE_NAME")
    
    @classmethod
    def DB_PASSWORD(cls) -> str:
        return os.getenv("DATABASE_PASSWORD")
    
    @classmethod
    def HOST(cls) -> str:
        return os.getenv("HOST")
    
    @classmethod
    def USER(cls) -> str:
        return os.getenv("USER")
    
    @classmethod
    def PORT(cls) -> str:
        return os.getenv("PORT")
    
    @classmethod
    def SECRET_KEY(cls) -> str:
        return os.getenv("SECRET_KEY")
    
    @classmethod
    def MODE(cls) -> str:
        return os.getenv("MODE")
