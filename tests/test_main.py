from fastapi.testclient import TestClient

from db_api.main import app

client = TestClient(app)


def test_no_auth():
    r = client.get("/users/me")
    assert r.status_code == 200
    assert r.json() == {"bla"}


def test_create_auth_user():
    assert False
