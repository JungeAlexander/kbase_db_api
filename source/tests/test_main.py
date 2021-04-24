from typing import Dict

from fastapi.testclient import TestClient

from db_api.core.config import settings

from .utils import random_email, random_lower_string


def test_no_auth(client: TestClient):
    r = client.get(f"{settings.API_V1_STR}/users/me")
    assert r.status_code == 401, r.text


def test_wrong_username_password(client: TestClient):
    data_dict = {"username": "nonxistingtestuser", "password": "meaninglesspassword"}
    r = client.post(f"{settings.API_V1_STR}/token", data=data_dict)
    assert r.status_code == 401, r.text


def test_create_auth_user(client: TestClient, superuser_token_headers: Dict[str, str]):
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    # create random user
    user_dict = {"email": email, "username": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", json=user_dict, headers=superuser_token_headers
    )
    assert r.status_code == 200, r.text
    # get token
    data_dict = {"username": username, "password": password}
    r = client.post(f"{settings.API_V1_STR}/token", data=data_dict)
    assert r.status_code == 200, r.text
    j = r.json()
    assert "access_token" in j, j
    # request user info
    header_dict = {"Authorization": f"{j['token_type']} {j['access_token']}"}
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=header_dict)
    j = r.json()
    assert j["email"] == email, j
    assert j["username"] == username, j
