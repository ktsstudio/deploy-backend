from _hashlib import HASH
from unittest.mock import patch

import pytest

from server.apps.user.models import User
from server.store import Store
from tests.apps.user import user2dict
from tests.conftest import authenticate


class TestUserRegister:
    async def test_validation(self, cli):
        resp = await cli.post("/user.register")
        document = await resp.json()
        assert document == {
            "password": ["Missing data for required field."],
            "username": ["Missing data for required field."],
        }

    async def test_success(self, cli, store: Store):
        resp = await cli.post(
            "/user.register", json={"password": "password", "username": "username"}
        )
        document = await resp.json()
        user = await store.user.get_by_username("username")
        assert user.password != "password"
        assert document == {"data": user2dict(user)}

    @pytest.mark.usefixtures("user1")
    async def test_already_exists(self, cli, store: Store):
        resp = await cli.post(
            "/user.register", json={"password": "password", "username": "username"}
        )
        document = await resp.json()
        assert resp.status == 400
        assert document == {"code": "already_exists", "description": "Already exists"}


class TestUserLogin:
    @pytest.mark.usefixtures("user1")
    async def test_user_does_not_exist(self, cli):
        with patch.object(HASH, "hexdigest", return_value="test") as mock_method:
            resp = await cli.post(
                "/user.login", json={"password": "password1", "username": "username1"}
            )
            assert not mock_method.called
        assert resp.status == 400
        document = await resp.json()
        assert document == {
            "code": "invalid_credentials",
            "description": "Username or password mismatch",
        }

    async def test_incorrect_password(self, cli, user1: User):
        with patch.object(HASH, "hexdigest", return_value="test") as mock_method:
            resp = await cli.post(
                "/user.login",
                json={"password": "incorrect", "username": user1.username},
            )
            assert mock_method.called

        assert resp.status == 400

    async def test_success(self, cli, user1: User):
        resp = await cli.post(
            "/user.login", json={"password": "password", "username": user1.username}
        )
        assert resp.status == 200
        assert "session_id" in cli.session.cookie_jar._cookies["127.0.0.1"]


class TestUserMe:
    async def test_not_authorized(self, cli):
        resp = await cli.get("/user.me")
        assert resp.status == 401

    async def test_success(self, cli, store, user1):
        async with authenticate(cli, store, user1):
            resp = await cli.get("/user.me")
        assert resp.status == 200


class TestUserTest:
    async def test_success(self, cli, mock_response):
        mock_response.get("http://httpbin.org/get", payload="payload")
        resp = await cli.get("/user.test")
        document = await resp.json()
        assert document == {"data": {"body": '"payload"', "status": 200}}
