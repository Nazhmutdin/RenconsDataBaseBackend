import pytest
import json

from app.db.session import Base, engine
from app.settings import Settings

from app.domain import WelderShema, WelderCertificationShema


settings = Settings()


@pytest.fixture(scope="session", autouse=True)
def prepare_db():
    assert settings.MODE() == "TEST"

    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def welders() -> list[WelderShema]:
    welders_json = json.load(open("test/test_welders.json", "r", encoding="utf-8"))

    return [WelderShema.model_validate(welder) for welder in welders_json]


@pytest.fixture
@pytest.mark.usefixtures('welders')
def welder_certifications(welders: list[WelderShema]) -> list[WelderCertificationShema]:
    certifications = []

    for welder in welders:
        certifications += welder.certifications

    return certifications
