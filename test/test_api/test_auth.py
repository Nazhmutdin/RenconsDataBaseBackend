from client import client
from httpx import Cookies
from datetime import datetime
import pytest
import json


@pytest.mark.run(order=3)
@pytest.mark.usefixtures("add_users")
class TestAuthEndpoints:

    def test_login(self):
        response = client.post("/auth/login", json={
            "login": "TestUser",
            "password": "111222"
        })

        client.cookies = Cookies({"access_token": response.cookies.get("access_token")})

        assert response.status_code == 200
        assert datetime.fromisoformat(json.loads(response.text)["login_date"]).strftime("%Y-%m-%d %H:%M") == datetime.now().strftime("%Y-%m-%d %H:%M")


    def test_create_user(self):
        response = client.post("/auth/create-user", json={
            "login": "TestUser2",
            "password": "111333",
            "su_login": "TestUser",
            "su_password": "111222"
        })

        assert response.status_code == 201
        response = client.post("/auth/login", json={
            "login": "TestUser2",
            "password": "111333"
        })
        assert response.status_code == 200


    def test_update_user(self):
        response = client.post("/auth/update-user", json={
            "login": "TestUser2",
            "password": "111333",
            "email": "2121212",
            "su_login": "TestUser",
            "su_password": "111222"
        })

        assert response.status_code == 200
        response = client.post("/auth/login", json={
            "login": "TestUser2",
            "password": "111333"
        })
        assert response.status_code == 200
        assert json.loads(response.text)["email"] == "2121212"


    def test_delete_user(self):
        response = client.post("/auth/delete-user", json={
            "login": "TestUser2",
            "su_login": "TestUser",
            "su_password": "111222"
        })

        assert response.status_code == 200
        response = client.post("/auth/login", json={
            "login": "TestUser2",
            "password": "111333"
        })
        assert response.status_code == 401
