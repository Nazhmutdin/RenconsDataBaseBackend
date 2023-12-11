import pytest

from app.db.repository import WelderRepository
from app.domain import WelderShema


class TestWelderRepository:
    repo = WelderRepository()

    @pytest.mark.run(order=1)
    @pytest.mark.usefixtures('welders')
    def test_add_welder(self, welders: list[WelderShema]) -> None:
        for welder in welders:
            self.repo.add(welder)

        assert self.repo.count() == len(welders)


    @pytest.mark.parametrize(
            "id, expectation",
            [
                ("B0ME", WelderShema),
                ("1E41", WelderShema),
                ("93VH", WelderShema),
            ]
    )
    def test_res_is_welder_shema(self, id: int | str, expectation: WelderShema | None) -> None:
        assert type(self.repo.get(id)) == expectation

    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 3, 4, 5, 6]
    )
    def test_get_welder(self, index: int, welders: list[WelderShema]) -> None:
        welder = welders[index]
        assert self.repo.get(welder.kleymo) == welder


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 63, 4, 5, 11]
    )
    def test_add_with_existing_welder(self, welders: list[WelderShema], index: int) -> None:
        self.repo.add(welders[index])

        assert self.repo.count() == len(welders)

    
    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [1, 42, 76, 4, 33, 15]
    )
    def test_update_welder(self, welders: list[WelderShema], index: int) -> None:
        welder = welders[index]
        welder.name = f"Name_{index}"

        self.repo.update(welder)
        updated_welder = self.repo.get(welder.kleymo)
        assert updated_welder.name == welder.name


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete_welder(self, welders: list[WelderShema], index: int) -> None:
        welder = welders[index]

        self.repo.delete(welder)

        assert self.repo.get(welder.kleymo) == None
