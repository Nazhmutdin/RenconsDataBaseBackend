import pytest
import json

from client import client


@pytest.mark.run(order=4)
@pytest.mark.usefixtures("add_data")
class TestV1ApiEndpoints:

    @pytest.mark.parametrize(
            "id",
            ["1M65", "01M8", "04PC"]
    )
    def test_get_welder(self, id: str | int):

        response = client.get(f"/api/v1/welders/{id}")

        assert response.status_code == 200


    @pytest.mark.parametrize(
            "id",
            [
                "007bмр1гацi4291120230510", 
                "01e0бр1ацi0208220141007", 
                "01esсур16ацi0336920210714в1"
            ]
    )
    def test_get_welder_certification(self, id: str):

        response = client.get(f"/api/v1/welder-certifications/{id}")

        assert response.status_code == 200


    @pytest.mark.parametrize(
            "id",
            [
                "1hcsrhikipelectricalinstallationudokan20230904", 
                "0cz5sarenponderaalng220220719", 
                "13z7hsconstructionmetalyapiawp1b20210609"
            ]
    )
    def test_get_ndt(self, id: str):

        response = client.get(f"/api/v1/ndts/{id}")

        assert response.status_code == 200


    def test_create_welder(self):
        response = client.put(
            "/api/v1/welders/",
            json={
                "name": "TestWelder",
                "kleymo": "0000",
            }
        )

        assert response.status_code == 200

        assert client.get("/api/v1/welders/0000").status_code == 200


    # def test_create_welder_certification(self):
    #     response = client.put(
    #         "/api/v1/welder-certifications/",
    #         json={
    #             "name": "TestWelder",
    #             "kleymo": "0000",
    #         }
    #     )

    #     assert response.status_code == 200

    #     assert client.get("/api/v1/welders/0000").status_code == 200


    # def test_create_ndt(self):
    #     response = client.put(
    #         "/api/v1/welders/",
    #         json={
    #             "name": "TestWelder",
    #             "kleymo": "0000",
    #         }
    #     )

        assert response.status_code == 200

        assert client.get("/api/v1/welders/0000").status_code == 200


    def test_update_welder(self):
        response = client.patch(
            "/api/v1/welders/",
            json={
                "name": "TestWelder1",
                "kleymo": "0000",
                "birthday": "2000-11-18"
            }
        )

        res_json = json.loads(response.content)

        assert response.status_code == 200
        assert res_json["name"] == "TestWelder1"


    def test_delete_welder(self):
        response = client.delete("/api/v1/welders/0000")

        assert response.status_code == 200
        assert client.get("/api/v1/welders/0000").status_code == 400
