from fastapi.testclient import TestClient

from db_api.main import app

from .utils import random_email, random_lower_string

client = TestClient(app)


def test_no_auth():
    r = client.get("/me")
    assert r.status_code == 401, r.text


def test_wrong_username_password():
    data_dict = {"username": "nonxistingtestuser", "password": "meaninglesspassword"}
    r = client.post("/token", data=data_dict)
    assert r.status_code == 401, r.text


def test_create_auth_user():
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    # create random user
    user_dict = {"email": email, "username": username, "password": password}
    r = client.post("/users/", json=user_dict)
    assert r.status_code == 200, r.text
    # get token
    data_dict = {"username": username, "password": password}
    r = client.post("/token", data=data_dict)
    assert r.status_code == 200, r.text
    j = r.json()
    assert "access_token" in j, j
    # request user info
    header_dict = {"Authorization": f"{j['token_type']} {j['access_token']}"}
    r = client.get("/me", headers=header_dict)
    j = r.json()
    assert j["email"] == email, j
    assert j["username"] == username, j
