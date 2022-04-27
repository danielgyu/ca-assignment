from fastapi.testclient import TestClient
from pytest import MonkeyPatch
import pytest

from cookapps.app import app 
from cookapps.tests.conftest import count_table


pytestmark = pytest.mark.asyncio


@pytest.fixture
def client(populate_data: None):
    return TestClient(app)


async def test_user_register_success(client: TestClient) -> None:
    res = client.post(
        "/users/register",
        json={"username": "lee", "password": "satisfying-password"},
    )
    assert res.status_code == 200
    assert res.json() == dict(success=True, reason=None)


async def test_user_register_fail_constraint(
    client: TestClient
) -> None:
    res = client.post(
        "/users/register",
        json={"username": "lee", "password": "invalid"},
    )
    assert res.status_code == 200
    assert res.json() == dict(success=False, reason="Invalid password")


async def test_user_register_not_unique(client: TestClient):
    res = client.post(
        "/users/register",
        json={"username": "kim", "password": "satisfying-password"},
    )
    assert res.status_code == 200
    assert res.json() == dict(success=False, reason="Username already exists")


async def test_user_login_success(
    client: TestClient,
    monkeypatch: MonkeyPatch,
):
    monkeypatch.setattr(
        "cookapps.routes.make_token",
        lambda user_id: "token",
    )
    res = client.post(
        "/users/login",
        json={"username": "kim", "password": "satisfying-password"},
    )
    assert res.status_code == 200
    assert res.json() == dict(success=True, token="token")


async def test_user_login_failure_user_not_found(
    client: TestClient,
    monkeypatch: MonkeyPatch,
):
    monkeypatch.setattr(
        "cookapps.routes.make_token",
        lambda user_id: "token",
    )
    res = client.post(
        "/users/login",
        json={"username": "park", "password": "satisfying-password"},
    )
    assert res.status_code == 401
    assert res.json() == dict(success=False, token="")


async def test_user_login_failure_wrong_password(
    client: TestClient,
    monkeypatch: MonkeyPatch,
):
    monkeypatch.setattr(
        "cookapps.routes.make_token",
        lambda user_id: "token",
    )
    res = client.post(
        "/users/login",
        json={"username": "kim", "password": "wrong-password"},
    )
    assert res.status_code == 401
    assert res.json() == dict(success=False, token="")
