from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient

from db_api.main import app

from .utils import get_superuser_token_headers


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)
