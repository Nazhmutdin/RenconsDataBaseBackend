import pytest

from app.db.repository import WelderCertificationRepository
from app.domain import WelderCertificationShema, WelderShema


class TestWelderCertificationRepository:
    repo = WelderCertificationRepository()

    @pytest.mark.run(order=2)
    @pytest.mark.usefixtures('welder_certifications')
    def test_add_welder_certification(self, welder_certifications: list[WelderCertificationShema]) -> None:
        length = len(welder_certifications)
        for certification in welder_certifications:
            self.repo.add(certification)
        
        assert self.repo.count() == length

    
    @pytest.mark.parametrize(
            "id, expectation",
            [
                ("9ml3юр3гацi2192820220525", WelderCertificationShema),
                ("7r54юр3гацi1756720170913", WelderCertificationShema),
                ("c0lfюр9ацi0948320220418", WelderCertificationShema),
            ]
    )
    def test_res_is_welder_certification_shema(self, id: int | str, expectation: WelderCertificationShema | None) -> None:
        assert type(self.repo.get(id)) == expectation


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 3, 4, 5, 6]
    )
    def test_get_welder_certification(self, index: int, welder_certifications: list[WelderCertificationShema]) -> None:
        certification = welder_certifications[index]
        assert self.repo.get(certification.certification_id) == certification


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 311, 63, 31, 75, 150]
    )
    def test_add_with_existing_welder_certification(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        self.repo.add(welder_certifications[index])

        assert self.repo.count() == len(welder_certifications)

    
    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 42, 76, 170, 33, 15]
    )
    def test_update_welder_certification(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        certification = welder_certifications[index]
        certification.gtd = ["111", "222"]

        self.repo.update(certification)
        updated_certification = self.repo.get(certification.certification_id)
        assert updated_certification.gtd == certification.gtd


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete_welder_certification(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        certification = welder_certifications[index]

        self.repo.delete(certification)

        assert self.repo.get(certification.certification_id) == None
