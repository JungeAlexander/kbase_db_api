from fastapi.testclient import TestClient

from db_api.main import app

client = TestClient(app)


def test_no_auth():
    r = client.get("/me")
    assert r.status_code == 401, r.text


def test_wrong_username_password():
    data_dict = {"username": "nonxistingtestuser", "password": "meaninglesspassword"}
    r = client.post("/token", data=data_dict)
    assert r.status_code == 401, r.text


def test_create_auth_user():
    assert False
