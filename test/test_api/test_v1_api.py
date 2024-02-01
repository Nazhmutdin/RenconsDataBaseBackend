import pytest
import json

from client import client
from app.shemas import WelderShema, WelderCertificationShema, WelderNDTShema


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

    
    @pytest.mark.usefixtures("test_welders")
    def test_create_welder(self, test_welders: list[WelderShema]):
        for welder in test_welders:
            response = client.put(
                "/api/v1/welders/",
                json=welder.model_dump(mode="json")
            )
            assert response.status_code == 200

            assert client.get(f"/api/v1/welders/{welder.kleymo}").status_code == 200


    @pytest.mark.usefixtures("test_welder_certifications")
    def test_create_welder_certification(self, test_welder_certifications: list[WelderCertificationShema]):

        for cert in test_welder_certifications:
            response = client.put(
                "/api/v1/welder-certifications/",
                json=cert.model_dump(mode="json")
            )

            assert response.status_code == 200

            res_json = json.loads(client.get(f"/api/v1/welder-certifications/{cert.certification_id}").content)

            assert res_json["certification_id"] == cert.certification_id


    @pytest.mark.usefixtures("test_welder_ndts")
    def test_create_ndt(self, test_welder_ndts: list[WelderNDTShema]):
        for ndt in test_welder_ndts:
            response = client.put(
                "/api/v1/ndts/",
                json=ndt.model_dump(mode="json")
            )

            assert response.status_code == 200

            assert client.get(f"/api/v1/ndts/{ndt.ndt_id}").status_code == 200


    @pytest.mark.usefixtures("test_welders")
    def test_update_welder(self, test_welders: list[WelderShema]):

        for welder in test_welders:
            json_data = welder.model_dump(mode="json")
            json_data["name"] = "TestName"

            response = client.patch(
                "/api/v1/welders/",
                json=json_data
            )

            res_json = json.loads(response.content)

            assert response.status_code == 200
            assert res_json["name"] == "TestName"

    
    @pytest.mark.usefixtures("test_welder_certifications")
    def test_update_welder_certification(self, test_welder_certifications: list[WelderCertificationShema]):

        for cert in test_welder_certifications:
            json_data = cert.model_dump(mode="json")
            json_data["details_thikness_from"] = 10000

            response = client.patch(
                "/api/v1/welder-certifications/",
                json=json_data
            )

            res_json = json.loads(response.content)

            assert response.status_code == 200
            assert res_json["details_thikness_from"] == 10000

    
    @pytest.mark.usefixtures("test_welder_ndts")
    def test_update_ndt(self, test_welder_ndts: list[WelderNDTShema]):
        for ndt in test_welder_ndts:
            json_data = ndt.model_dump(mode="json")
            json_data["comp"] = "assds"
            response = client.patch(
                "/api/v1/ndts/",
                json=json_data
            )
            
            res_json = json.loads(response.content)

            assert response.status_code == 200
            assert res_json["comp"] == "assds"

    
    @pytest.mark.usefixtures("test_welder_certifications")
    def test_delete_welder_certification(self, test_welder_certifications: list[WelderCertificationShema]):
        for welder_certification in test_welder_certifications:
            response = client.delete(f"/api/v1/welder-certifications/{welder_certification.certification_id}")
            
            assert response.status_code == 200
            assert client.get(f"/api/v1/welder-certifications/{welder_certification.certification_id}").status_code == 400

    
    @pytest.mark.usefixtures("test_welder_ndts")
    def test_delete_ndt(self, test_welder_ndts: list[WelderNDTShema]):
        for welder_ndt in test_welder_ndts:
            response = client.delete(f"/api/v1/ndts/{welder_ndt.ndt_id}")

            assert response.status_code == 200
            assert client.get(f"/api/v1/ndts/{welder_ndt.ndt_id}").status_code == 400

    
    @pytest.mark.usefixtures("test_welders")
    def test_delete_welder(self, test_welders: list[WelderShema]):
        for welder in test_welders:
            response = client.delete(f"/api/v1/welders/{welder.kleymo}")

            assert response.status_code == 200
            assert client.get(f"/api/v1/welders/{welder.kleymo}").status_code == 400
