import pytest

from app.settings import Settings


settings = Settings()


@pytest.fixture(scope="function")
def access_token() -> dict[str, str]:
    return {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbiI6Ik5hemhtdXRkaW5HdW11ZXYiLCJwYXNzd29yZCI6IlFXRTEyM2RmIn0.T9ENknlG6OgEd4778cmr-TttJfsKshf14I6A2NbjIlI"
    }
