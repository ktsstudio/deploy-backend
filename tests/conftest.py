import copy
import datetime
import functools

import pytest
from aiohttp import CookieJar
from aioresponses import aioresponses
from dateutil import tz
from freezegun import freeze_time
from gino import GinoEngine

import settings
from server.store import Store

settings.config = settings.get_config(settings.BASE_DIR / "config" / "test.yaml")
from server.store.gino import db
from server.web.app import create_app
from tests.fixtures import *

DEFAULT_TIME = datetime.datetime(2020, 2, 15, 0, tzinfo=tz.UTC)


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def store(app):
    return app["store"]


@pytest.fixture
async def cli(aiohttp_client, app):
    client = await aiohttp_client(app)
    yield client


@pytest.fixture(autouse=True)
async def db_transaction(cli):
    real_acquire = GinoEngine.acquire

    async with db.acquire() as conn:

        class _AcquireContext:
            __slots__ = ["_acquire", "_conn"]

            def __init__(self, acquire):
                self._acquire = acquire

            async def __aenter__(self):
                return conn

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                pass

            def __await__(self):
                return conn

        def acquire(self, *, timeout=None, reuse=False, lazy=False, reusable=True):
            return _AcquireContext(
                functools.partial(self._acquire, timeout, reuse, lazy, reusable)
            )

        GinoEngine.acquire = acquire
        transaction = await conn.transaction()
        yield
        await transaction.rollback()
        GinoEngine.acquire = real_acquire


@pytest.fixture
def freeze_t():
    freezer = freeze_time(DEFAULT_TIME)
    freezer.start()
    yield DEFAULT_TIME
    freezer.stop()


@pytest.fixture(autouse=True)
async def mock_response():
    with aioresponses(passthrough=["http://127.0.0.1"]) as responses_mock:
        yield responses_mock


class authenticate:
    def __init__(self, cli, store: Store, user):
        self.cli = cli
        self.store = store
        self.user = user

    async def __aenter__(self):
        s = await self.store.session.generate_session(self.user.username)
        self.cli.session.cookie_jar.update_cookies({"session_id": s.id})

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.cli.session.cookie_jar.update_cookies({"session_id": ""})
