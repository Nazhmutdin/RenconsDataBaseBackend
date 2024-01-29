import pytest
import json

from client import client


@pytest.mark.run(order=4)
@pytest.mark.usefixtures("add_data")
class TestV1ApiEndpoints:

    def test_get_welder(self):

        response = client.get("/api/v1/welders/0324")

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
