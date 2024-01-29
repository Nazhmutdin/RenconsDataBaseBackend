from client import client
from httpx import Cookies
import pytest


@pytest.mark.run(order=3)
@pytest.mark.usefixtures("add_users")
class TestAuthEndpoints:

    def test_login(self):
        response = client.post("/login", json={
            "login": "TestUser",
            "password": "111222"
        })

        client.cookies = Cookies({"access_token": response.cookies.get("access_token")})

        assert response.status_code == 200
